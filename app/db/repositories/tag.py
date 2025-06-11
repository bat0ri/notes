from typing import Optional, List
from sqlalchemy.orm import Session
import uuid

from app.db.repositories.base import BaseRepository
from app.models.tag import Tag
from app.models.note import Note
from app.schemas.tag import TagCreate, TagUpdate


class TagRepository(BaseRepository[Tag, TagCreate, TagUpdate]):
    
    def get_by_name(self, db: Session, tag_name: str) -> Tag:

        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            return None
        return tag

    def create(self, db: Session, *, obj_in: TagCreate) -> Tag:
        db_obj = Tag(
            id=str(uuid.uuid4()),
            name=obj_in.name
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_tags_by_note(self, db: Session, note_id: str) -> List[Tag]:
        """
        Получение всех тегов заметки.
        """
        note = db.query(Note).filter(Note.id == note_id).first()
        if not note:
            return []
        return note.tags

    def add_tags_to_note(
        self,
        db: Session,
        *,
        note_id: str,
        tag_ids: List[str]
    ) -> List[Tag]:
        """
        Добавление тегов к заметке.
        
        Args:
            db: Сессия базы данных
            note_id: ID заметки
            tag_ids: Список ID тегов для добавления
            
        Returns:
            List[Tag]: Список добавленных тегов
            
        Raises:
            ValueError: Если заметка не найдена
        """
        note = db.query(Note).filter(Note.id == note_id).first()
        if not note:
            raise ValueError(f"Note with id {note_id} not found")
            
        # Получаем теги по ID
        tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
        
        # Добавляем только те теги, которых еще нет у заметки
        for tag in tags:
            if tag not in note.tags:
                note.tags.append(tag)
                
        db.add(note)
        db.commit()
        db.refresh(note)
        
        return tags

    def get_or_create(self, db: Session, *, name: str) -> Tag:
        tag = self.get_by_name(db, name=name)
        if not tag:
            tag = self.create(db, obj_in=TagCreate(name=name))
        return tag 