from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.associations import note_tags
 
class Tag(Base):
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    notes = relationship('Note', secondary=note_tags, back_populates='tags') 