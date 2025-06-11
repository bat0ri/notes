from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.api import deps
from app.schemas.note import Note, NoteCreate, NoteUpdate, NoteUpdateExternal
from app.services.note import NoteService
from app.services.tag import TagService

router = APIRouter()


@router.get("/", response_model=List[Note])
def read_notes(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 20,
    note_service: NoteService = Depends(deps.get_note_service)
) -> List[Note]:
    """
    Получение списка заметок с пагинацией
    """ 
    return note_service.get_list(db=db, skip=skip, limit=limit)

@router.get("/{note_id}", response_model=Note)
def read_note(
    *,
    db: Session = Depends(deps.get_db),
    note_id: str,
    note_service: NoteService = Depends(deps.get_note_service)
) -> Note:
    """
    Получение заметки по ID.
    """
    note = note_service.get(db=db, id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.post("/", response_model=Note)
def create_note(
    *,
    db: Session = Depends(deps.get_db),
    note_in: NoteCreate,
    note_service: NoteService = Depends(deps.get_note_service)
) -> Note:
    """
    Создание новой заметки.
    """
    return note_service.create_with_tags(db=db, obj_in=note_in)


@router.patch("/{note_id}", response_model=Note)
def patch_note(
    *,
    db: Session = Depends(deps.get_db),
    note_id: str,
    note_in: NoteUpdate,
    note_service: NoteService = Depends(deps.get_note_service)
) -> Note:
    """
    Patch заметки.
    - тег добавляется по айди (если существует)
    """
    note = note_service.patch(db=db, note_id=note_id, obj_in=note_in)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=Note)
def update_note(
    *,
    db: Session = Depends(deps.get_db),
    note_id: str,
    note_in: NoteUpdateExternal,
    note_service: NoteService = Depends(deps.get_note_service)
) -> Note:
    """
    Обновление заметки -> + удаление тегов, если не указать
    """
    note = note_service.update(db=db, note_id=note_id, obj_in=note_in)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.delete("/{note_id}", response_model=Note)
def delete_note(
    *,
    db: Session = Depends(deps.get_db),
    note_id: str,
    note_service: NoteService = Depends(deps.get_note_service)
) -> Note:
    """
    Удаление заметки.
    """
    note = note_service.remove(db=db, id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
