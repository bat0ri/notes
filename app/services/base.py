from typing import Generic, TypeVar, Type, List, Optional, Dict
from sqlalchemy.orm import Session

from app.db.repositories.base import BaseRepository

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    def get(self, db: Session, id: str) -> ModelType:
        return self.repository.get(db=db, id=id)

    def get_list(
        self, db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: dict = {}
    ) -> list[ModelType]:
        return self.repository.get_list(
            db=db, filters=filters, skip=skip, limit=limit)
    
    def get_list_by_ids(
        self, db: Session, ids: List[str]
    ) -> list[ModelType]:
        return self.repository.get_list_by_ids(db=db, ids=ids)

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        return self.repository.create(db=db, obj_in=obj_in)

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        return self.repository.update(db=db, db_obj=db_obj, obj_in=obj_in)

    def remove(self, db: Session, *, id: str) -> ModelType:
        return self.repository.remove(db=db, id=id) 