from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from apps.auth.src.dto import UserLoginReqBody
from apps.auth.src.service import auth_service
from libs.utils.jwt.src.helpers import jwt_helpers

auth_route = APIRouter(prefix='/auth', tags=['Authentication'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@auth_route.post('/login')
def auth_login(request_data: UserLoginReqBody):
    try:
        access_token = auth_service.generate_token(request_data)
        return JSONResponse(
            {'message': 'Login Successful', 'access_token': access_token}, 200
        )
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error message: {str(e)}'
        )


@auth_route.post('/logout')
def auth_logout(access_token: str = Depends(jwt_helpers.is_token_valid)):
    try:
        auth_service.remove_token(access_token)
        return {'message': 'Logout successful'}, 200
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error message: {str(e)}'
        )
