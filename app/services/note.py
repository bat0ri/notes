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

    def create_with_tags(
        self, db: Session, *, obj_in: NoteCreate
    ) -> Note:
        try:
            existing_tags = self.tag_repository.get_list_by_ids(db=db, ids=obj_in.tags)
            
            note_data = obj_in.model_dump(exclude={'tags'})
            note = self.repository.create(db=db, obj_in=note_data)
            note.tags.extend(existing_tags)
            db.commit()
            db.refresh(note)
            
            return note
            
        except Exception as e:
            db.rollback()
            raise ValueError(f"Не удалось создать заметку с тегами: {str(e)}")

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
        
        tags = self.tag_repository.get_list_by_ids(db=db, ids=obj_in.tags)

        # Обновляем заметку
        updated_note = self.repository.update_with_tags(
            db=db,
            db_obj=note,
            obj_in=obj_in,
            tags=tags
        )
        
        return updated_note
    
    def update(
        self,
        db: Session,
        *,
        note_id: str,
        obj_in: NoteUpdateExternal
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
        
        
        ids = [t.id for t in obj_in.tags]
        tags = self.tag_repository.get_list_by_ids(db=db, ids=ids)
        note.tags = []
        db.flush()  # Фиксируем удаление старых тегов
        
        # Добавляем новые теги по одному
        for tag in tags:
            note.tags.append(tag)

        # Обновляем заметку
        updated_note = self.repository.update(
            db=db,
            db_obj=note,
            obj_in=obj_in
        )
        
        return updated_note 