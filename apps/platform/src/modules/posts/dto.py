from pydantic import BaseModel


class NewPostReqBody(BaseModel):
    postId: str
    postDescription: str


class UpdatePostReqBody(BaseModel):
    postDescription: str
