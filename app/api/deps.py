from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.db.repositories.note import NoteRepository
from app.db.repositories.tag import TagRepository
from app.models.note import Note
from app.models.tag import Tag

settings = get_settings()

# Будет использоваться для Keycloak
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_note_repository() -> NoteRepository:
    return NoteRepository(Note)


def get_tag_repository() -> TagRepository:
    return TagRepository(Tag)


# Будет использоваться для Keycloak
async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Optional[dict]:
    """
    Получение текущего пользователя из токена.
    Будет реализовано после интеграции с Keycloak.
    """
    # TODO: Implement Keycloak integration
    return {"id": "test-user-id", "username": "test-user"} 