from typing import List, Optional
from sqlalchemy.orm import Session

from app.db.repositories.base import BaseRepository
from app.models.image import Image
from app.schemas.image import ImageCreate


class ImageRepository(BaseRepository[Image, ImageCreate, ImageCreate]):
    def get_by_note(self, db: Session, *, note_id: str) -> List[Image]:
        return db.query(self.model).filter(self.model.note_id == note_id).all()

    def get_by_id(self, db: Session, *, id: str) -> Optional[Image]:
        return db.query(self.model).filter(self.model.id == id).first() 
    
    def get_by_short_url(self, db: Session, *, short_url: str) -> Optional[Image]:
        return db.query(self.model).filter(self.model.short_url == short_url).first()
    
    