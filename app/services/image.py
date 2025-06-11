from typing import List, Optional
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.db.repositories.image import ImageRepository
from app.db.repositories.note import NoteRepository
from app.models.image import Image
from app.schemas.image import ImageCreate
from app.services.base import BaseService
from app.storage.minio import storage
from app.utils.url import get_unique_short_url


class ImageService(BaseService[Image, ImageCreate, ImageCreate]):
    def __init__(
        self,
        image_repository: ImageRepository,
        note_repository: NoteRepository
    ):
        super().__init__(image_repository)
        self.note_repository = note_repository

    async def upload_image(
        self, db: Session, *, note_id: str, file: UploadFile
    ) -> Image:
        """
        Загружает изображение в MinIO и создает запись в базе данных
        """
        # Проверяем существование заметки
        note = self.note_repository.get(db=db, id=note_id)
        if not note:
            raise HTTPException(
                status_code=404,
                detail="Note not found"
            )

        # Проверяем тип файла
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File must be an image"
            )

        try:
            # Загружаем файл в MinIO
            url = await storage.upload_file(file=file, note_id=note_id)
            
            # Генерируем короткий URL
            short_url = get_unique_short_url(db=db, url=url, note_id=note_id)

            # Создаем запись в базе данных
            image_in = ImageCreate(
                filename=file.filename,
                url=url,
                short_url=short_url,
                content_type=file.content_type
            )
            
            db_obj = Image(
                **image_in.model_dump(),
                note_id=note_id
            )
            
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            
            return db_obj
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload image: {str(e)}"
            )

    def get_by_note(self, db: Session, *, note_id: str) -> List[Image]:
        """
        Получает все изображения для заметки
        """
        return self.repository.get_by_note(db=db, note_id=note_id)

    def get_by_short_url(self, db: Session, *, short_url: str) -> Image:
        """
        Получает все изображения по короткому URL
        """
        return self.repository.get_by_short_url(db=db, short_url=short_url)

    async def delete_image(self, db: Session, *, image_id: str) -> None:
        """
        Удаляет изображение из MinIO и базы данных
        """
        image = self.get(db=db, id=image_id)
        if not image:
            raise HTTPException(
                status_code=404,
                detail="Image not found"
            )

        try:
            # Удаляем файл из MinIO, используя правильный путь
            object_name = f"{image.note_id}/{image.filename}"
            await storage.delete_file(object_name)

            # Удаляем запись из базы данных
            db.delete(image)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete image: {str(e)}"
            ) 