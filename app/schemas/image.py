from datetime import datetime
from pydantic import BaseModel, HttpUrl


class ImageBase(BaseModel):
    filename: str
    url: HttpUrl
    short_url: str
    content_type: str


class ImageCreate(ImageBase):
    pass


class ImageInDB(ImageBase):
    id: str
    note_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class Image(ImageInDB):
    pass 