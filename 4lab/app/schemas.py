from datetime import datetime
from pydantic import BaseModel, Field, validator

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

    @validator("name")
    def name_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Имя не должно быть пустым")
        return v.strip()

class UserResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}

class PostCreate(BaseModel):
    text: str = Field(..., min_length=1)
    user_id: int

    @validator("text")
    def text_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Текст не должен быть пустым")
        return v.strip()

class PostUpdate(BaseModel):
    text: str = Field(..., min_length=1)

    @validator("text")
    def text_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Текст не должен быть пустым")
        return v.strip()

class PostResponse(BaseModel):
    id: int
    text: str
    date_of_creation: datetime
    user_id: int

    model_config = {"from_attributes": True}
