from flask import Blueprint, abort, make_response
from flask_jwt_extended import jwt_required

from apps.auth.modules.service import auth_service

auth_blueprint = Blueprint("Authentication", __name__, url_prefix="/auth")


@auth_blueprint.post("/login")
def auth_login():
    try:
        access_token = auth_service.generate_token()

        return make_response(access_token, 200)
    except Exception as e:
        abort(500, message=f"Error message: {str(e)}")


@auth_blueprint.post("/logout")
@jwt_required()
def auth_logout():
    try:
        auth_service.remove_token()

        return make_response({"message": "Logout successful"}, 200)
    except Exception as e:
        abort(500, message=f"Error message: {str(e)}")
