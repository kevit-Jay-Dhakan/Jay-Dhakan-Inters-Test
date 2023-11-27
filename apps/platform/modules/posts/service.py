from datetime import datetime

from bson.objectid import ObjectId
from flask import request
from flask_jwt_extended import get_jwt
from marshmallow import ValidationError

from apps.platform.modules.posts.dto import PostSchema
from libs.domains.posts.repository import posts_repository
from libs.domains.users.repository import users_repository


class PostsService:
    @staticmethod
    def find_post(post_id: str):
        try:
            post_data = posts_repository.find_one({"post_id": post_id})
            post_data["_id"] = str(post_data["_id"])

            return post_data
        except Exception as e:
            return {"message": f"Error message: {str(e)}"}

    @staticmethod
    def find_posts():
        try:
            user = get_jwt()["sub"]
            user = users_repository.find_one({"_id": ObjectId(user)})
            user_id = user["user_id"]

            posts_data = list(posts_repository.find_many({"user_id": user_id}))
            for post in posts_data:
                post["_id"] = str(post["_id"])

            return posts_data
        except Exception as e:
            return {"message": f"Error message: {str(e)}"}

    @staticmethod
    def insert_post():
        user = get_jwt()["sub"]
        user = users_repository.find_one({"_id": ObjectId(user)})
        user_id = user["user_id"]

        try:
            post_data = request.get_json()

            try:
                PostSchema().load(post_data)

            except ValidationError as e:
                return {"Validation errors": e.messages}

            post_id = post_data["post_id"]
            post_description = post_data["post_description"]

            if posts_repository.find_one({"post_id": post_id}):
                return {"message": f"post_id {post_id} already exists "}

            posts_repository.insert_one(
                {
                    "post_id": post_id,
                    "user_id": user_id,
                    "post_description": post_description,
                    "createdAt": datetime.now(),
                    "updatedAt": datetime.now()
                }
            )

            return {"message": f"Post created successfully."}
        except Exception as e:
            return {"message": f"Error message: {str(e)}"}

    @staticmethod
    def update_post():
        try:
            post_data = request.get_json()
            if post_data == {}:
                return {"message": "Looks like you changed your mind to update"}

            try:
                PostSchema().load(post_data)

            except ValidationError as e:
                return {"Validation errors": e.messages}

            post_id = post_data["post_id"]
            post_description = post_data["post_description"]

            posts_repository.update_one(
                {"post_id": post_id},
                {
                    "$set": {
                        "post_description": post_description,
                        "updatedAt": datetime.now(),
                    }
                },
            )
            updated_post = posts_repository.find_one({"post_id": post_id})
            updated_post["_id"] = str(updated_post["_id"])

            return updated_post
        except Exception as err:
            return {"message": f"Error :: {str(err)}"}

    @staticmethod
    def delete_post():
        try:
            post_id = request.get_json()["post_id"]
            post_exists = posts_repository.find_one({"post_id": post_id})

            if post_exists is None:
                return {"message": "Post does not exist, please try again!!"}
            else:
                posts_repository.delete_one({"post_id": post_id})

                return {"message": f"Post Deleted successfully."}
        except Exception as e:
            return {"message": f"Error message: {str(e)}"}


posts_service = PostsService()
