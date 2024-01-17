from pydantic import BaseModel


class UserLoginReqBody(BaseModel):
    userId: str
    password: str
