from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base
from app.models.associations import note_tags

class Note(Base):
    __tablename__ = "note"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    version = Column(Integer, default=1, nullable=False)
    # lazy="dynamic"
    tags = relationship('Tag', secondary=note_tags, back_populates='notes', lazy="dynamic")
    images = relationship("Image", back_populates="note", cascade="all, delete-orphan") 