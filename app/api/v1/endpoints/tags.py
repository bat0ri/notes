from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.tag import Tag, TagCreate, TagUpdate
from app.services.tag import TagService

router = APIRouter()


@router.get("/", response_model=List[Tag])
def read_tags(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    tag_service: TagService = Depends(deps.get_tag_service)
) -> List[Tag]:
    """
    Получение списка тегов.
    """
    return tag_service.get_list(db=db, skip=skip, limit=limit)


@router.post("/", response_model=Tag)
def create_tag(
    *,
    db: Session = Depends(deps.get_db),
    tag_in: TagCreate,
    tag_service: TagService = Depends(deps.get_tag_service)
) -> Tag:
    """
    Создание нового тега.
    """
    tag = tag_service.get_by_name(db=db, tag_name=tag_in.name)
    if tag:
        raise HTTPException(
            status_code=400,
            detail="Tag with this name already exists"
        )
    return tag_service.create(db=db, obj_in=tag_in)


@router.delete("/{tag_id}", response_model=Tag)
def delete_tag(
    *,
    db: Session = Depends(deps.get_db),
    tag_id: str,
    tag_service: TagService = Depends(deps.get_tag_service)
) -> Tag:
    """
    Удаление тега.
    """
    tag = tag_service.remove(db=db, id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.put("/{tag_id}", response_model=Tag)
def update_tag(
    *,
    db: Session = Depends(deps.get_db),
    tag_id: str,
    tag_in: TagUpdate,
    tag_service: TagService = Depends(deps.get_tag_service)
) -> Tag:
    """
    Обновление тега.
    
    - Если новое имя тега уже существует, вернет ошибку 400
    - Если тег не найден, вернет ошибку 404
    """
    # Проверяем существование тега
    tag = tag_service.get(db=db, id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    # Если передано новое имя, проверяем что оно не занято
    if tag_in.name is not None and tag_in.name != tag.name:
        existing_tag = tag_service.get_by_name(db=db, name=tag_in.name)
        if existing_tag:
            raise HTTPException(
                status_code=400,
                detail="Tag with this name already exists"
            )
    
    # Обновляем тег
    updated_tag = tag_service.update(db=db, db_obj=tag, obj_in=tag_in)
    return updated_tag