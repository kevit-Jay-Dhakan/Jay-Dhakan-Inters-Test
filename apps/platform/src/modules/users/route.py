from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from apps.platform.src.modules.users.dto import RegisterUserReqBody
from apps.platform.src.modules.users.service import users_service

users_route = APIRouter(prefix='/users', tags=['Users'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@users_route.get("/<string:user_id>")
def get_user(user_id: str):
    try:
        user = users_service.find_user(user_id)
        return {"user data": user}, 200
    except Exception as e:
        HTTPException(500, detail=f"Error :: {str(e)}")


@users_route.post("/register_user")
def register_user(request_data: RegisterUserReqBody):
    try:
        inserted_user = users_service.register_user(request_data)
        return inserted_user, 200
    except Exception as e:
        HTTPException(500, detail=f"Error :: {str(e)}")


@users_route.post("/update_user")
def update_user(access_token: str = Depends(oauth2_scheme)):
    try:
        updated_user = users_service.update_user(access_token)
        return updated_user, 200
    except Exception as e:
        HTTPException(500, detail=f"Error :: {str(e)}")


@users_route.delete("/delete_user")
def delete(access_token: str = Depends(oauth2_scheme)):
    try:
        deleted_user = users_service.delete_user(access_token)
        return deleted_user, 201
    except Exception as e:
        HTTPException(500, detail=f"Error :: {str(e)}")
