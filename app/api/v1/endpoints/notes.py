from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.note import Note, NoteCreate, NoteUpdate
from app.db.repositories.note import NoteRepository
from app.db.repositories.tag import TagRepository

router = APIRouter()


@router.post("/", response_model=Note)
def create_note(
    *,
    db: Session = Depends(deps.get_db),
    note_in: NoteCreate,
    note_repo: NoteRepository = Depends(deps.get_note_repository),
    tag_repo: TagRepository = Depends(deps.get_tag_repository),
) -> Note:
    """
    Создание новой заметки.
    """
    # Создаем или получаем существующие теги
    tag_ids = []
    for tag_name in note_in.tags:
        tag = tag_repo.get_or_create(db, name=tag_name)
        tag_ids.append(tag.id)
    
    note = note_repo.create_with_tags(db=db, obj_in=note_in, tag_ids=tag_ids)
    return note


@router.get("/", response_model=List[Note])
def read_notes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    tag: Optional[str] = None,
    note_repo: NoteRepository = Depends(deps.get_note_repository),
) -> List[Note]:
    """
    Получение списка заметок.
    """
    if tag:
        notes = note_repo.get_by_tag(db=db, tag_name=tag, skip=skip, limit=limit)
    else:
        notes = note_repo.get_multi(db=db, skip=skip, limit=limit)
    return notes


@router.get("/{note_id}", response_model=Note)
def read_note(
    *,
    db: Session = Depends(deps.get_db),
    note_id: str,
    note_repo: NoteRepository = Depends(deps.get_note_repository),
) -> Note:
    """
    Получение заметки по ID.
    """
    note = note_repo.get(db=db, id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=Note)
def update_note(
    *,
    db: Session = Depends(deps.get_db),
    note_id: str,
    note_in: NoteUpdate,
    note_repo: NoteRepository = Depends(deps.get_note_repository),
    tag_repo: TagRepository = Depends(deps.get_tag_repository),
) -> Note:
    """
    Обновление заметки.
    """
    note = note_repo.get(db=db, id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    tag_ids = None
    if note_in.tags is not None:
        tag_ids = []
        for tag_name in note_in.tags:
            tag = tag_repo.get_or_create(db, name=tag_name)
            tag_ids.append(tag.id)
    
    note = note_repo.update_with_tags(
        db=db, db_obj=note, obj_in=note_in, tag_ids=tag_ids
    )
    return note


@router.delete("/{note_id}")
def delete_note(
    *,
    db: Session = Depends(deps.get_db),
    note_id: str,
    note_repo: NoteRepository = Depends(deps.get_note_repository),
) -> dict:
    """
    Удаление заметки.
    """
    note = note_repo.get(db=db, id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note_repo.remove(db=db, id=note_id)
    return {"status": "success"} 