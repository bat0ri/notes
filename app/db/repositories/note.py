from typing import List, Optional
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from app.db.repositories.base import BaseRepository
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate


class NoteRepository(BaseRepository[Note, NoteCreate, NoteUpdate]):
    def create_with_tags(
        self, db: Session, *, obj_in: NoteCreate, tag_ids: List[str]
    ) -> Note:
        db_obj = Note(
            id=str(uuid.uuid4()),
            title=obj_in.title,
            content=obj_in.content,
            version=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        # Добавляем теги
        for tag_id in tag_ids:
            tag = db.query(Note).filter(Note.id == tag_id).first()
            if tag:
                db_obj.tags.append(tag)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_tag(
        self, db: Session, *, tag_name: str, skip: int = 0, limit: int = 100
    ) -> List[Note]:
        return (
            db.query(self.model)
            .join(self.model.tags)
            .filter(Note.name == tag_name)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_with_tags(
        self,
        db: Session,
        *,
        db_obj: Note,
        obj_in: NoteUpdate,
        tag_ids: Optional[List[str]] = None
    ) -> Note:
        update_data = obj_in.dict(exclude_unset=True)
        
        if tag_ids is not None:
            db_obj.tags = []
            for tag_id in tag_ids:
                tag = db.query(Note).filter(Note.id == tag_id).first()
                if tag:
                    db_obj.tags.append(tag)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db_obj.version += 1
        db_obj.updated_at = datetime.utcnow()
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj 