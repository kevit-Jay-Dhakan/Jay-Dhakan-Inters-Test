from pydantic import BaseModel, Field


class NewPostReqBody(BaseModel):
    postId: str = Field(
        description='Id of post.',
        example='jay1',
        min_length=1,
        max_length=30
    )
    postDescription: str = Field(
        description="Post's description.",
        example='This post is created in memory of first api project.',
        min_length=1,
        max_length=200
    )


class UpdatePostReqBody(BaseModel):
    postDescription: str = Field(
        description="Post's description.",
        example='This post is created in memory of first api project.',
        min_length=1,
        max_length=200
    )
