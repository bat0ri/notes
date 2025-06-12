from typing import List, Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session
import uuid

from app.db.repositories.image import ImageRepository
from app.db.repositories.note import NoteRepository
from app.models.image import Image
from app.schemas.image import ImageCreate
from app.services.base import BaseService
from app.storage.minio import storage
from app.utils.url import get_unique_short_url
from app.core.exceptions import NotFoundException, StorageException, DatabaseException


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
        note = self.note_repository.get(db=db, id=note_id)
        if not note:
            raise NotFoundException(f"Заметка с id {note_id} не найдена")

        try:
            # Генерируем уникальное имя файла
            file_extension = file.filename.split('.')[-1] if file.filename else 'jpg'
            filename = f"{uuid.uuid4()}.{file_extension}"
            object_name = f"{note_id}/{filename}"

            # Загружаем файл в MinIO
            try:
                await storage.upload_file(
                    file=file,
                    object_name=object_name
                )
            except Exception as e:
                raise StorageException(f"Не удалось загрузить файл: {str(e)}")

            # Создаем запись в базе данных
            try:
                short_url = await get_unique_short_url()
                image_in = ImageCreate(
                    filename=filename,
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
                # Если не удалось создать запись в БД, удаляем файл из хранилища
                try:
                    await storage.delete_file(object_name)
                except:
                    pass
                raise DatabaseException(f"Не удалось создать запись в базе данных: {str(e)}")

        except Exception as e:
            db.rollback()
            if isinstance(e, (StorageException, DatabaseException)):
                raise
            raise DatabaseException(f"Неожиданная ошибка при загрузке изображения: {str(e)}")

    def get_by_note(self, db: Session, *, note_id: str) -> List[Image]:
        """
        Получает все изображения для заметки
        """
        return self.repository.get_by_note(db=db, note_id=note_id)

    def get_by_short_url(self, db: Session, *, short_url: str) -> Image:
        """
        Получает изображение по короткому URL
        """
        image = self.repository.get_by_short_url(db=db, short_url=short_url)
        if not image:
            raise NotFoundException(f"Изображение с коротким URL {short_url} не найдено")
        return image

    async def delete_image(self, db: Session, *, image_id: str) -> None:
        """
        Удаляет изображение из MinIO и базы данных
        """
        image = self.get(db=db, id=image_id)
        if not image:
            raise NotFoundException(f"Изображение с id {image_id} не найдено")

        try:
            # Удаляем файл из MinIO
            object_name = f"{image.note_id}/{image.filename}"
            try:
                await storage.delete_file(object_name)
            except Exception as e:
                raise StorageException(f"Не удалось удалить файл из хранилища: {str(e)}")

            # Удаляем запись из базы данных
            try:
                db.delete(image)
                db.commit()
            except Exception as e:
                raise DatabaseException(f"Не удалось удалить запись из базы данных: {str(e)}")

        except Exception as e:
            db.rollback()
            if isinstance(e, (StorageException, DatabaseException)):
                raise
            raise DatabaseException(f"Неожиданная ошибка при удалении изображения: {str(e)}") 