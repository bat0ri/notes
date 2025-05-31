from typing import Optional
from pydantic import BaseModel, Field


class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    name: Optional[str] = Field(None, min_length=1, max_length=50)


class TagInDBBase(TagBase):
    id: str
    note_count: int = 0

    class Config:
        from_attributes = True


class Tag(TagInDBBase):
    pass


class TagInDB(TagInDBBase):
    pass 