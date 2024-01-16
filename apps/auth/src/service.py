from datetime import datetime, timedelta, timezone

from bson.objectid import ObjectId
from fastapi import HTTPException, status
from jose import jwt
from passlib.hash import pbkdf2_sha256

from apps.auth.src.dto import UserLoginReqBody
from libs.domains.auth.src.repository import auth_repository
from libs.util.common.src.modules.enums import Role
from libs.util.jwt.src.jwt_config import (
    ACCESS_TOKEN_EXPIRE_IN_MINUTES, ALGORITHM, SECRET_KEY
)


class AuthService:
    @staticmethod
    def add_privilege_claims_to_jwt(user_oid):
        user = auth_repository.find_one({'_id': ObjectId(user_oid)})

        claims = {'is_admin': False, 'is_super_admin': False}
        if user and 'privilege' in user:
            privilege = user['privilege']
            if privilege == Role.ADMIN.value:
                claims['is_admin'] = True
            elif privilege == Role.SUPER_ADMIN.value:
                claims['is_admin'] = True
                claims['is_super_admin'] = True

        return claims

    def create_access_token(self, data: dict):
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_IN_MINUTES)
        expires_at = datetime.now(timezone.utc) + expires_delta
        data_with_claims = {
            **data, **self.add_privilege_claims_to_jwt(data.get('identity'))
        }
        to_encode = {'exp': expires_at, **data_with_claims}
        return jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    def generate_token(self, request_date: UserLoginReqBody):
        user = auth_repository.find_one({'user_id': request_date.user_id})
        user_oid = str(user['_id'])
        if user and pbkdf2_sha256.verify(
            request_date.password, user['password']
        ):
            access_token = self.create_access_token({'identity': user_oid})
            auth_repository.update_one(
                {'_id': ObjectId(user_oid)}, {'$push': {'tokens': access_token}}
            )
            return access_token
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid credentials'
            )

    @staticmethod
    def decode_jwt_token(access_token: str):
        return jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])

    def remove_token(self, access_token: str):
        try:
            payload = self.decode_jwt_token(access_token)
            current_user_oid = payload.get('identity')
            if not access_token or not current_user_oid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Invalid token'
                )

            auth_repository.update_one(
                {'_id': ObjectId(current_user_oid)},
                {'$pull': {'tokens': access_token}}
            )

            return {'message': 'Logout successful'}
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'message': f'Error :: {str(err)}'}
            )


auth_service = AuthService()
