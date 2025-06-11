from typing import Optional
from sqlalchemy.orm import Session

from app.db.repositories.tag import TagRepository
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate
from app.services.base import BaseService


class TagService(BaseService[Tag, TagCreate, TagUpdate]):
    def __init__(self, repository: TagRepository):
        super().__init__(repository)

    def get_by_name(self, db: Session, *, tag_name: str) -> Optional[Tag]:
        """
        Получение тега по имени.
        """
        return self.repository.get_by_name(db=db, tag_name=tag_name)

    def get_or_create(self, db: Session, *, name: str) -> Tag:
        """
        Получение существующего тега или создание нового.
        """
        return self.repository.get_or_create(db=db, name=name) 