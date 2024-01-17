from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from apps.platform.src.modules.posts.dto import (
    NewPostReqBody, UpdatePostReqBody
)
from apps.platform.src.modules.posts.service import posts_service
from libs.utils.jwt.src.helpers import jwt_helpers

posts_route = APIRouter(prefix='/posts', tags=['Posts'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@posts_route.get('/get_post/{post_id}')
def get_post(
    post_id: str, access_token: str = Depends(jwt_helpers.is_token_valid)
):
    post = posts_service.find_post(post_id, access_token)
    return post, 200


@posts_route.get('/get_all_posts')
def get_posts(access_token: str = Depends(jwt_helpers.is_token_valid)):
    posts = posts_service.find_posts(access_token)
    return posts, 200


@posts_route.post('/create_post')
def create_post(
    new_post_data: NewPostReqBody,
    access_token: str = Depends(jwt_helpers.is_token_valid)
):
    created_post = posts_service.insert_post(new_post_data, access_token)
    return created_post, 200


@posts_route.post('/update_post/{post_id}')
def update_post(
    post_id: str, update_post_data: UpdatePostReqBody,
    access_token: str = Depends(jwt_helpers.is_token_valid)
):
    updated_post = posts_service.update_post(
        post_id, update_post_data, access_token
    )
    return updated_post, 200


@posts_route.delete('/delete_post/{post_id}')
def delete_post(
    post_id: str, access_token: str = Depends(jwt_helpers.is_token_valid)
):
    deleted_post = posts_service.delete_post(post_id, access_token)
    return deleted_post, 201
