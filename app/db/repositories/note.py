from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
import uuid
from datetime import datetime

from app.db.repositories.base import BaseRepository
from app.models.note import Note
from app.models.tag import Tag
from app.schemas.note import NoteCreate, NoteUpdate


class NoteRepository(BaseRepository[Note, NoteCreate, NoteUpdate]):
    
    def update_with_tags(
        self,
        db: Session,
        *,
        db_obj: Note,
        obj_in: NoteUpdate,
        tags: List[Tag]
    ) -> Note:
        """
        Обновление заметки с существующими тегами.
        """
        for t in tags:
            db_obj.tags.append(t)
        
        update_data = obj_in.model_dump(exclude_unset=True, exclude={"tags"})
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db_obj.version += 1
        db_obj.updated_at = datetime.now()
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj