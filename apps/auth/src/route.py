import uvicorn
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from apps.auth.src.dto import UserLoginReqBody
from apps.auth.src.service import auth_service

auth_route = APIRouter(prefix='/auth', tags=['Authentication'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@auth_route.post("/login")
def auth_login(request_data: UserLoginReqBody):
    try:
        access_token = auth_service.generate_token(request_data)
        return {
            'message': 'Login Successful',
            'access_token': access_token
        }, 200
    except Exception as e:
        HTTPException(500, detail=f"Error message: {str(e)}")


@auth_route.post("/logout")
def auth_logout(access_token: str = Depends(oauth2_scheme)):
    try:
        auth_service.remove_token(access_token)
        return {"message": "Logout successful"}, 200
    except Exception as e:
        HTTPException(500, detail=f"Error message: {str(e)}")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Register user endpoint


if __name__ == '__main__':
    uvicorn.run('main:app', port=5000, reload=True)
