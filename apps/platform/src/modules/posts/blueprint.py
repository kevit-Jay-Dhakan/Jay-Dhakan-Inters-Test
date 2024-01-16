from flask import Blueprint, abort, make_response
from flask_jwt_extended import jwt_required

from apps.platform.src.modules.posts.service import posts_service

posts_blueprint = Blueprint("Posts", __name__, url_prefix="/posts")


@posts_blueprint.get("/<string:post_id>")
@jwt_required(fresh=True)
def get_post(post_id: str):
    try:
        user = posts_service.find_post(post_id)

        return make_response({"data": user}, 200)
    except Exception as e:
        abort(500, message=f"error message : {str(e)}")


@posts_blueprint.get("/users_all_posts")
@jwt_required(fresh=True)
def get_posts():
    try:
        user = posts_service.find_posts()

        return make_response({"data": user}, 200)
    except Exception as e:
        abort(500, message=f"error message : {str(e)}")


@posts_blueprint.post("/create_post")
@jwt_required(fresh=True)
def create_post():
    try:
        created_post = posts_service.insert_post()

        return make_response(created_post, 200)
    except Exception as e:
        abort(500, message=f"Error message: {str(e)}")


@posts_blueprint.post("/update_post")
@jwt_required(fresh=True)
def update_post():
    try:
        updated_post = posts_service.update_post()

        return make_response(updated_post, 200)
    except Exception as e:
        abort(500, message=f"Error :: {str(e)}")


@posts_blueprint.delete("/delete_post")
@jwt_required(fresh=True)
def delete_post():
    try:
        deleted_post = posts_service.delete_post()

        return make_response(deleted_post, 201)
    except Exception as e:
        abort(500, message=f"Error message: {str(e)}")
