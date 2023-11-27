from datetime import datetime

from bson.objectid import ObjectId
from flask import request
from flask_jwt_extended import get_jwt
from marshmallow import ValidationError
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from apps.platform.modules.users.dto import RegisterSchema, UpdateSchema
from libs.domains.auth.enums import Role
from libs.domains.auth.privileges import check_admin_privileges
from libs.domains.posts.repository import posts_repository
from libs.domains.users.repository import users_repository


class UsersService:
    @staticmethod
    def find_user(userid: str):
        try:
            user_data = users_repository.find_one({"_id": ObjectId(userid)})
            user_data["_id"] = str(user_data["_id"])
            return user_data

        except Exception as e:
            return {"message": f"Error message: {str(e)}"}

    @staticmethod
    def find_users():
        try:
            if not check_admin_privileges() == Role.SUPER_ADMIN.value:
                return {"message": "Super admin Privileges required"}

            users_data = list(users_repository.find_many({}))
            for user in users_data:
                user["_id"] = str(user["_id"])
            return users_data

        except Exception as e:
            return {"message": f"Error message: {str(e)}"}

    @staticmethod
    def insert_user():
        try:
            user_data = request.get_json()

            try:
                RegisterSchema().load(user_data)
            except ValidationError as err:
                return {"Validation errors": err.messages}

            user_id = user_data["user_id"]
            first_name = user_data["first_name"]
            last_name = user_data["last_name"]
            password = user_data["password"]
            privilege = user_data["privilege"]
            email = user_data["email"]

            if users_repository.find_one({"user_id": user_id}):
                return {"message": f"user_id {user_id} already exists "}

            if users_repository.find_one({"email": email}):
                return {"message": f"Email {email} already exists "}

            hashed_password = pbkdf2_sha256.hash(password)

            users_repository.insert_one(
                {
                    "user_id": user_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "password": hashed_password,
                    "email": email,
                    "privilege": privilege,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            )

            return {"message": f"User created successfully."}

        except Exception as err:
            return {"message": f"Error :: {str(err)}"}

    @staticmethod
    def update_user():
        try:
            user_id = get_jwt()["sub"]

            user_data = request.get_json()

            if user_data == {}:
                return {"message": "Looks like you changed your mind to update"}

            try:
                UpdateSchema().load(user_data)
            except ValidationError as err:
                return {"Validation errors": err.messages}

            first_name = user_data["first_name"]
            last_name = user_data["last_name"]

            users_repository.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$set": {
                        "first_name": first_name,
                        "last_name": last_name,
                        "updatedAt": datetime.now(),
                    }
                },
            )
            updated_user = users_repository.find_one({"_id": ObjectId(user_id)})
            updated_user["_id"] = str(updated_user["_id"])

            return updated_user

        except Exception as err:
            return {"message": f"Error :: {str(err)}"}

    @staticmethod
    def delete_user():
        try:
            user_id = get_jwt()["sub"]
            print(user_id)
            user_exists = users_repository.find_one({"_id": ObjectId(user_id)})

            if user_exists is None:
                return {
                    "message": "User does not exist, please login again and "
                               "try again!!"
                }

            else:
                users_repository.delete_one({"_id": ObjectId(user_id)})
                posts_repository.delete_many({"user_id": user_id})
                return {"message": f"User Deleted successfully."}

        except Exception as err:
            return {"message": f"Error :: {str(err)}"}


users_service = UsersService()
