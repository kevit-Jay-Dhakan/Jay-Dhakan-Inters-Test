from bson.objectid import ObjectId
from fastapi import HTTPException, status

from apps.platform.src.modules.posts.dto import (
    NewPostReqBody,
    UpdatePostReqBody
)
from libs.domains.posts.src.repository import posts_repository
from libs.utils.jwt.src.helpers import jwt_helpers
from libs.utils.logger.src import logger


class PostsService:
    @staticmethod
    def find_post(post_id: str, access_token: str):
        try:
            post = posts_repository.find_one({'postId': post_id})
            if post and access_token:
                post['_id'] = str(post['_id'])
                post['userOid'] = str(post['userOid'])
                return {'data': post}
            raise HTTPException(
                201, f'postId: {post_id} does not exists.'
            )
        except Exception as err:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

    @staticmethod
    def find_posts(access_token: str):
        try:
            payload = jwt_helpers.decode_jwt_token(access_token)
            current_user_oid = payload.get('identity')

            posts_data = list(
                posts_repository.find(
                    {'userOid': ObjectId(current_user_oid)}
                )
            )
            if len(posts_data) > 0:
                for post in posts_data:
                    post['_id'] = str(post['_id'])
                    post['userOid'] = str(post['userOid'])
                    return {'posts': posts_data}
            raise HTTPException(
                201,
                f'You have not created any posts. userOid: {current_user_oid}'
            )
        except Exception as err:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

    @staticmethod
    def insert_post(new_post_data: NewPostReqBody, access_token: str):
        try:
            payload = jwt_helpers.decode_jwt_token(access_token)
            current_user_oid = payload.get('identity')

            post_id = new_post_data.postId
            post_description = new_post_data.postDescription

            if posts_repository.find_one({'postId': post_id}):
                raise HTTPException(
                    201, f'postId: {post_id} already exists'
                )

            posts_repository.insert_one(
                {
                    'postId': post_id,
                    'userOid': ObjectId(current_user_oid),
                    'postDescription': post_description
                }
            )
            logger.debug(
                f'User with userOid: {current_user_oid} created one post.',
                send_in_ms_teams=True
            )
            return {'message': f'Post created successfully.'}
        except Exception as err:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

    @staticmethod
    def update_post(
        post_id: str, update_post_data: UpdatePostReqBody, access_token: str
    ):
        try:
            post_description = update_post_data.postDescription
            post = posts_repository.find_one({'postId': post_id})
            if post and access_token:
                posts_repository.update_one(
                    {'postId': post_id},
                    {'$set': {'postDescription': post_description}},
                )
                updated_post = posts_repository.find_one({'postId': post_id})
                updated_post['_id'] = str(updated_post['_id'])
                updated_post['userOid'] = str(updated_post['userOid'])
                return {
                    'message': 'Post Updated successfully', 'data': updated_post
                }, 200
            raise HTTPException(
                201, f'postId: {post_id} does not exists.'
            )
        except Exception as err:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

    @staticmethod
    def delete_post(post_id: str, access_token: str):
        try:
            post_exists = posts_repository.find_one({'postId': post_id})
            if post_exists and access_token:
                posts_repository.delete_one({'postId': post_id})
                logger.debug(
                    f'Post with postId: {post_id} was deleted',
                    send_in_ms_teams=True
                )
                return {
                    'message': f'Post with postId: {post_id}, '
                               f'deleted successfully.'
                }
            raise HTTPException(
                201, 'Post does not exist, please try again!!'
            )
        except Exception as err:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )


posts_service = PostsService()
