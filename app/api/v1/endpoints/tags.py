from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.tag import Tag, TagCreate, TagUpdate
from app.db.repositories.tag import TagRepository

router = APIRouter()


@router.get("/", response_model=List[Tag])
def read_tags(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    tag_repo: TagRepository = Depends(deps.get_tag_repository),
) -> List[Tag]:
    """
    Получение списка тегов.
    """
    tags = tag_repo.get_multi(db=db, skip=skip, limit=limit)
    return tags


@router.post("/", response_model=Tag)
def create_tag(
    *,
    db: Session = Depends(deps.get_db),
    tag_in: TagCreate,
    tag_repo: TagRepository = Depends(deps.get_tag_repository),
) -> Tag:
    """
    Создание нового тега.
    """
    tag = tag_repo.get_by_name(db=db, name=tag_in.name)
    if tag:
        raise HTTPException(
            status_code=400,
            detail="Tag with this name already exists"
        )
    tag = tag_repo.create(db=db, obj_in=tag_in)
    return tag


@router.delete("/{tag_id}")
def delete_tag(
    *,
    db: Session = Depends(deps.get_db),
    tag_id: str,
    tag_repo: TagRepository = Depends(deps.get_tag_repository),
) -> dict:
    """
    Удаление тега.
    """
    tag = tag_repo.get(db=db, id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag_repo.remove(db=db, id=tag_id)
    return {"status": "success"} 