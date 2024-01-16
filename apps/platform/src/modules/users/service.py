from datetime import datetime

from passlib.handlers.pbkdf2 import pbkdf2_sha256

from apps.platform.src.modules.users.dto import (
    RegisterUserReqBody
)
from libs.domains.users.src.repository import users_repository


class UsersService:
    @staticmethod
    def register_user(request_data: RegisterUserReqBody):
        try:
            user_id = request_data.user_id
            email = request_data.email
            if users_repository.find_one({'user_id': user_id}):
                return {'message': f'user_id {user_id} already exists'}

            if users_repository.find_one({'email': email}):
                return {'message': f'Email {email} already exists'}

            hashed_password = pbkdf2_sha256.hash(request_data.password)

            users_repository.insert_one(
                {
                    "user_id": user_id,
                    "first_name": request_data.first_name,
                    "last_name": request_data.last_name,
                    "password": hashed_password,
                    "email": email,
                    "privilege": request_data.privilege,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            )
            return {'message': f'User created successfully.'}
        except Exception as err:
            return {'message': f'Error :: {str(err)}'}


users_service = UsersService()
