from flask import abort, Blueprint, make_response
from flask_jwt_extended import jwt_required

from apps.platform.modules.users.service import users_service

users_blueprint = Blueprint("Users", __name__, url_prefix="/users")


@users_blueprint.get("/")
@jwt_required(fresh=True)
def get_users():
    try:
        users = users_service.find_users()

        return make_response({"data": users}, 200)
    except Exception as e:
        abort(500, message=f"error message : {str(e)}")


@users_blueprint.get("/<string:user_id>")
def get_user(user_id: str):
    try:
        user = users_service.find_user(user_id)

        return make_response({"data": user}, 200)
    except Exception as e:
        abort(500, message=f"Error :: {str(e)}")


@users_blueprint.post("/register_user")
def register_user():
    try:
        inserted_user = users_service.insert_user()

        return make_response(inserted_user, 200)
    except Exception as e:
        abort(500, message=f"Error :: {str(e)}")


@users_blueprint.post("/update_user")
@jwt_required(fresh=True)
def update_user():
    try:
        updated_user = users_service.update_user()

        return make_response(updated_user, 200)
    except Exception as e:
        abort(500, message=f"Error :: {str(e)}")


@users_blueprint.delete("/delete_user")
@jwt_required(fresh=True)
def delete():
    try:
        deleted_user = users_service.delete_user()

        return make_response(deleted_user, 201)
    except Exception as e:
        abort(500, message=f"Error :: {str(e)}")
