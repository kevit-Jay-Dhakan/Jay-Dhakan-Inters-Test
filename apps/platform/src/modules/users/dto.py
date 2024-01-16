from pydantic import BaseModel, EmailStr, Field


class RegisterUserReqBody(BaseModel):
    user_id: str = Field(
        description=''
    )
    first_name: str
    last_name: str
    password: str
    privilege: str
    email: EmailStr
