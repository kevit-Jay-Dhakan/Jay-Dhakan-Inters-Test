from datetime import datetime, timedelta, timezone

from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from libs.domains.users.src.repository import users_repository
from libs.utils.common.src.modules.enums import Role
from libs.utils.jwt.src.jwt_config import (
    ACCESS_TOKEN_EXPIRE_IN_MINUTES, ALGORITHM, JWT_SECRET_KEY
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class JwtHelpers:
    @staticmethod
    def add_privilege_claims_to_jwt(user_oid):
        user = users_repository.find_one({'_id': ObjectId(user_oid)})

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
        expires_delta = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_IN_MINUTES
        )
        data_with_claims = {
            **data, **self.add_privilege_claims_to_jwt(data.get('identity'))
        }
        to_encode = {'exp': expires_delta, **data_with_claims}
        return jwt.encode(to_encode, key=JWT_SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_jwt_token(access_token: str):
        return jwt.decode(access_token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

    def is_token_valid(self, access_token: str = Depends(oauth2_scheme)):
        try:
            payload = self.decode_jwt_token(access_token)
            current_user_id = payload.get('identity')

            user = users_repository.find_one(
                {
                    '_id': ObjectId(current_user_id),
                    'tokens': {'$elemMatch': {'$eq': access_token}}
                }
            )

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid access_token, please log in and try again!'
                )
            return access_token
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access_token'
            )

    def get_users_privileges(self, access_token: str = Depends(oauth2_scheme)):
        payload = self.decode_jwt_token(access_token)
        is_admin = payload.get('is_admin')
        is_super_admin = payload.get('is_super_admin')

        if is_super_admin:
            return Role.SUPER_ADMIN
        elif is_admin:
            return Role.ADMIN
        else:
            return Role.CUSTOMER


jwt_helpers = JwtHelpers()
