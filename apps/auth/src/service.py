from bson.objectid import ObjectId
from fastapi import HTTPException, status
from passlib.hash import pbkdf2_sha256

from apps.auth.src.dto import UserLoginReqBody
from libs.domains.users.src.repository import users_repository
from libs.utils.jwt.src.helpers import jwt_helpers


class AuthService:
    @staticmethod
    def generate_token(request_date: UserLoginReqBody):
        user = users_repository.find_one({'userId': request_date.userId})
        if user and pbkdf2_sha256.verify(
            request_date.password, user['password']
        ):
            user_oid = str(user['_id'])
            access_token = jwt_helpers.create_access_token(
                {'identity': user_oid}
            )
            users_repository.update_one(
                {'_id': ObjectId(user_oid)}, {'$push': {'tokens': access_token}}
            )
            return access_token
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid credentials'
            )

    @staticmethod
    def remove_token(access_token: str):
        try:
            payload = jwt_helpers.decode_jwt_token(access_token)
            current_user_oid = payload.get('identity')
            if not access_token or not current_user_oid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Invalid token'
                )

            users_repository.update_one(
                {'_id': ObjectId(current_user_oid)},
                {'$pull': {'tokens': access_token}}
            )
            return {'message': 'Logout successful'}
        except Exception as err:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Error message: {str(err)}'
            )


auth_service = AuthService()
