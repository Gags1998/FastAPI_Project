from pydantic import BaseModel, ConfigDict, Field

class PostBase(BaseModel):
    title: str = Field(..., max_length=100)
    content: str = Field(..., max_length=500)
    author: str = Field(..., max_length=50)

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_posted: str
