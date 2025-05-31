from typing import Optional
from sqlalchemy.orm import Session
import uuid

from app.db.repositories.base import BaseRepository
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate


class TagRepository(BaseRepository[Tag, TagCreate, TagUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Tag]:
        return db.query(self.model).filter(self.model.name == name).first()

    def create(self, db: Session, *, obj_in: TagCreate) -> Tag:
        db_obj = Tag(
            id=str(uuid.uuid4()),
            name=obj_in.name
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_or_create(self, db: Session, *, name: str) -> Tag:
        tag = self.get_by_name(db, name=name)
        if not tag:
            tag = self.create(db, obj_in=TagCreate(name=name))
        return tag 