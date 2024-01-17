from pydantic import BaseModel, EmailStr, Field


class RegisterUserReqBody(BaseModel):
    userId: str = Field(
        description=''
    )
    firstName: str
    lastName: str
    password: str
    privilege: str
    email: EmailStr


class UpdateUserReqBody(BaseModel):
    firstName: str = Field(
        description='',
        default=None
    )
    lastName: str = Field(
        description='',
        default=None
    )
    password: str = Field(
        description='',
        default=None
    )
