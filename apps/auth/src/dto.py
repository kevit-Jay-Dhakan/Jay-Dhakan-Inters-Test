from pydantic import BaseModel


class UserLoginReqBody(BaseModel):
    user_id: str
    password: str
