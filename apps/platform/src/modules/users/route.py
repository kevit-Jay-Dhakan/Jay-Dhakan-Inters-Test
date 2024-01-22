from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordBearer

from apps.platform.src.modules.users.dto import (
    RegisterUserReqBody, UpdateUserReqBody
)
from apps.platform.src.modules.users.service import users_service
from libs.utils.jwt.src.helpers import jwt_helpers
from libs.utils.limiter.src.helpers import limiter

users_route = APIRouter(prefix='/users', tags=['Users'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@users_route.get('/')
@limiter.limit('5/minute')
def get_users(
    request: Request,
    access_token: str = Depends(jwt_helpers.is_token_valid)
):
    users = users_service.find_users(access_token)
    return users


@users_route.get('/{user_id}')
def get_user(user_id: str):
    user = users_service.find_user(user_id)
    return user, 200


@users_route.post('/register_user')
def register_user(new_user_data: RegisterUserReqBody):
    inserted_user = users_service.register_user(new_user_data)
    return inserted_user, 200


@users_route.post('/update_user')
def update_user(
    update_user_data: UpdateUserReqBody,
    access_token: str = Depends(jwt_helpers.is_token_valid)
):
    updated_user = users_service.update_user(access_token, update_user_data)
    return updated_user, 200


@users_route.delete('/delete_user')
def delete(access_token: str = Depends(jwt_helpers.is_token_valid)):
    deleted_user = users_service.delete_user(access_token)
    return deleted_user, 201
