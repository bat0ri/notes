from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from app.db.repositories.note import NoteRepository
from app.db.repositories.tag import TagRepository
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate, NoteUpdateExternal
from app.services.base import BaseService


class NoteService(BaseService[Note, NoteCreate, NoteUpdate]):
    def __init__(
        self,
        note_repository: NoteRepository,
        tag_repository: TagRepository
    ):
        super().__init__(note_repository)
        self.tag_repository = tag_repository

    def patch(
        self,
        db: Session,
        *,
        note_id: str,
        obj_in: NoteUpdate
    ) -> Optional[Note]:
        """
        Обновление заметки с тегами и контентом.
        - Если переданы теги, они заменяют существующие. Теги по айди
        - Если тег не существует, он пропускается
        - Если теги не переданы, существующие теги сохраняются
        - Контент и заголовок обновляются, если переданы
        """
        note = self.repository.get(db=db, id=note_id)
        if not note:
            return None
        
        updated_note = note
        if obj_in.tags is not None and len(obj_in.tags) != 0:
            # если теги предали, то добавляем теги
            tag_ids = [t["id"] for t in obj_in.tags]
            tags = self.tag_repository.get_list_by_ids(db=db, ids=tag_ids)
            updated_note = self.repository.update(
                db=db,
                db_obj=note,
                obj_in=obj_in,
                tags=tags
            )
        else:
            updated_note = self.repository.update(
                db=db,
                db_obj=note,
                obj_in=obj_in
            )
        
        return updated_note
 