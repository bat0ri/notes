from typing import Generator, Optional, Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.db.repositories.note import NoteRepository
from app.db.repositories.tag import TagRepository
from app.db.repositories.image import ImageRepository
from app.models.note import Note
from app.models.tag import Tag
from app.models.image import Image
from app.services.note import NoteService
from app.services.tag import TagService
from app.services.image import ImageService

settings = get_settings()

# Будет использоваться для Keycloak
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")


def get_db() -> Generator:
    """
    Зависимость для получения сессии базы данных.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_note_repository() -> NoteRepository:
    """
    Зависимость для получения репозитория заметок.
    """
    return NoteRepository(Note)


def get_tag_repository() -> TagRepository:
    """
    Зависимость для получения репозитория тегов.
    """
    return TagRepository(Tag)


def get_image_repository() -> ImageRepository:
    return ImageRepository(Image)


def get_note_service(
    note_repository: Annotated[NoteRepository, Depends(get_note_repository)],
    tag_repository: Annotated[TagRepository, Depends(get_tag_repository)]
) -> NoteService:
    """
    Зависимость для получения сервиса заметок.
    """
    return NoteService(note_repository=note_repository, tag_repository=tag_repository)


def get_tag_service(
    tag_repository: Annotated[TagRepository, Depends(get_tag_repository)]
) -> TagService:
    """
    Зависимость для получения сервиса тегов.
    """
    return TagService(repository=tag_repository)


def get_image_service(
    image_repository: Annotated[ImageRepository, Depends(get_image_repository)],
    note_repository: Annotated[NoteRepository, Depends(get_note_repository)]
) -> ImageService:
    return ImageService(
        image_repository=image_repository,
        note_repository=note_repository
    )


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