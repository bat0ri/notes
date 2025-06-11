from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False)
    url = Column(String, nullable=False)
    short_url = Column(String, unique=True, nullable=False)
    content_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связь с заметкой
    note_id = Column(String, ForeignKey("note.id", ondelete="CASCADE"), nullable=False)
    note = relationship("Note", back_populates="images") 