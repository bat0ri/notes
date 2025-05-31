from sqlalchemy import Column, String, ForeignKey, Table

from app.db.base import Base

# Таблица связи между заметками и тегами
note_tags = Table(
    'note_tags',
    Base.metadata,
    Column('note_id', String, ForeignKey('note.id')),
    Column('tag_id', String, ForeignKey('tag.id'))
) 