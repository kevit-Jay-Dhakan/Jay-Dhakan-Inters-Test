from datetime import datetime, timedelta

import jwt
from bson.objectid import ObjectId
from flask import request
from flask_jwt_extended import create_access_token, get_jwt
from libs.domains.auth.repository import auth_repository
from libs.utils.jwt.config import JWT_SECRET_KEY
from marshmallow import ValidationError
from passlib.hash import pbkdf2_sha256

from apps.auth.modules.dto import AuthSchema


class AuthService:
    @staticmethod
    def generate_token():
        try:
            login_data = request.get_json()

            try:
                AuthSchema().load(login_data)

            except ValidationError as e:
                return {"Validation errors": e.messages}

            user_id = login_data["user_id"]
            password = login_data["password"]

            # Find the user by user_id
            user = auth_repository.find_one({"user_id": user_id})

            if not user:
                return {"message": "User not found"}
            user_id = str(user["_id"])

            if pbkdf2_sha256.verify(password, user["password"]):
                expiration_time = datetime.utcnow() + timedelta(
                    minutes=30
                )  # user_expire_time
                access_token = create_access_token(
                    identity=user_id,
                    fresh=True,
                    expires_delta=expiration_time - datetime.utcnow(),
                )
                if "tokens" not in user:
                    user["tokens"] = []

                decoded_token = jwt.decode(
                    access_token, JWT_SECRET_KEY, algorithms=["HS256"]
                )

                jti = decoded_token.get("jti")
                auth_repository.update_one(
                    {"_id": ObjectId(user_id)}, {"$push": {"tokens": jti}}
                )

                return {"message": "Login successful", "access_token": access_token}
            else:
                return {"message": "Invalid password"}

        except Exception as e:
            return {"message": f"Error :: {str(e)}"}

    @staticmethod
    def remove_token():
        try:
            jti = get_jwt()["jti"]
            current_user_id = get_jwt()["sub"]

            auth_repository.update_one(
                {"_id": ObjectId(current_user_id)}, {"$pull": {"tokens": jti}}
            )

            return "Logout successful"

        except Exception as e:
            return f"Error :: {str(e)}"


auth_service = AuthService()
