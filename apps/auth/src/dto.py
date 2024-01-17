from pydantic import BaseModel, Field


class UserLoginReqBody(BaseModel):
    userId: str = Field(
        description="User's id.",
        example='jaydhakan1234',
        min_length=1,
        max_length=20
    )
    password: str = Field(
        description='Your password',
        example='xyz1234',
        min_length=1,
        max_length=20
    )
