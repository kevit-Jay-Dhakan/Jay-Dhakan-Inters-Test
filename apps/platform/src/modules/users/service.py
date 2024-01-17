from bson import ObjectId
from fastapi import HTTPException, status
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from apps.platform.src.modules.users.dto import (
    RegisterUserReqBody, UpdateUserReqBody
)
from libs.domains.posts.src.repository import posts_repository
from libs.domains.users.src.repository import users_repository
from libs.utils.common.src.modules.enums import Role
from libs.utils.jwt.src.helpers import jwt_helpers
from libs.utils.logger.src import logger


class UsersService:
    @staticmethod
    def find_users(access_token: str):
        try:
            if not (
                jwt_helpers.get_users_privileges(access_token) ==
                Role.SUPER_ADMIN
            ):
                raise HTTPException(201, f'Super admin Privileges required')

            users_data = list(users_repository.find({}))
            for user in users_data:
                user['_id'] = str(user['_id'])
            return {'users': users_data}
        except Exception as e:
            return {'message': f'Error message: {str(e)}'}

    @staticmethod
    def find_user(user_id: str):
        try:
            user = users_repository.find_one(
                {'_id': ObjectId(user_id)}, {'password': 0}
            )
            user['_id'] = str(user['_id'])
            return {'user': user}
        except Exception as err:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Error message: {str(err)}'
            )

    @staticmethod
    def register_user(new_user_data: RegisterUserReqBody):
        try:
            user_id = new_user_data.userId
            email = new_user_data.email
            if users_repository.find_one({'userId': user_id}):
                raise HTTPException(201, f'userId: {user_id} already exists')

            if users_repository.find_one({'email': email}):
                raise HTTPException(201, f'Email: {email} already exists')

            hashed_password = pbkdf2_sha256.hash(new_user_data.password)

            users_repository.insert_one(
                {
                    'userId': user_id,
                    'firstName': new_user_data.firstName,
                    'lastName': new_user_data.lastName,
                    'password': hashed_password,
                    'email': email,
                    'privilege': new_user_data.privilege
                }
            )
            return {'message': f'User created successfully.'}
        except Exception as err:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

    @staticmethod
    def update_user(access_token, update_user_data: UpdateUserReqBody):
        try:
            payload = jwt_helpers.decode_jwt_token(access_token)
            current_user_oid = payload.get('identity')

            if update_user_data.model_dump() == {}:
                return HTTPException(
                    201, 'Looks like you changed your mind to update'
                )

            user = users_repository.find_one(
                {'_id': ObjectId(current_user_oid)}
            )
            first_name = user['firstName'] if (
                update_user_data.firstName is None) else (
                update_user_data.firstName)
            last_name = user['lastName'] if (
                update_user_data.lastName is None) else (
                update_user_data.lastName)
            password = user['password'] if (
                update_user_data.password is None) else (
                pbkdf2_sha256.hash(update_user_data.password))

            users_repository.update_one(
                {'_id': ObjectId(current_user_oid)},
                {
                    '$set': {
                        'firstName': first_name,
                        'lastName': last_name,
                        'password': password
                    }
                }
            )
            updated_user = users_repository.find_one(
                {'_id': ObjectId(current_user_oid)}, {'password': 0}
            )
            updated_user['_id'] = str(updated_user['_id'])
            logger.debug(
                f'User {user["firstName"] + user["lastName"]} updated their '
                f'account details', send_in_ms_teams=True
            )
            return updated_user
        except Exception as err:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

    @staticmethod
    def delete_user(access_token):
        try:
            payload = jwt_helpers.decode_jwt_token(access_token)
            current_user_oid = payload.get('identity')

            user = users_repository.find_one(
                {'_id': ObjectId(current_user_oid)}
            )
            if user:
                users_repository.delete_one({'_id': ObjectId(current_user_oid)})
                posts_repository.delete_many(
                    {'userOid': ObjectId(current_user_oid)}
                )
                logger.info(
                    f'User {user['firstName'] + user['lastName']} deleted '
                    f'their account.', send_in_ms_teams=True
                )
                return {'message': f'User Deleted successfully.'}
            else:
                raise HTTPException(
                    201,
                    'User does not exist, please login again and try again!!'
                )
        except Exception as err:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )


users_service = UsersService()
