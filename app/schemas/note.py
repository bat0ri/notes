from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .tag import Tag


class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    tags: Optional[List[dict]] = None


class NoteUpdateExternal(NoteUpdate):
    tags: List[Tag]
    

class NoteInDBBase(NoteBase):
    id: str
    created_at: datetime
    updated_at: datetime
    version: int
    tags: List[Tag] = []

    class Config:
        from_attributes = True


class Note(NoteInDBBase):
    pass


class NoteInDB(NoteInDBBase):
    pass 