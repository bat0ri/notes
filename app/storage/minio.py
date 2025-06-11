from typing import Optional, BinaryIO, AsyncGenerator
from contextlib import asynccontextmanager
from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from botocore.client import Config
from fastapi import UploadFile, HTTPException
import aiofiles
import os
from datetime import datetime, timedelta
import uuid
import json

from app.core.config import get_settings

settings = get_settings()


class MinioStorage:
    def __init__(self):
        self.config = {
            "aws_access_key_id": settings.MINIO_ROOT_USER,
            "aws_secret_access_key": settings.MINIO_ROOT_PASSWORD,
            "endpoint_url": f"http://{settings.MINIO_SERVER}:{settings.MINIO_PORT}",
            "region_name": "us-east-1",  # MinIO требует указания региона
            "config": Config(signature_version='s3v4')
        }
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self.session = get_session()

    @asynccontextmanager
    async def create_client(self) -> AsyncGenerator:
        """Создает клиент S3 с использованием контекстного менеджера"""
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def _ensure_bucket_exists(self) -> None:
        """Проверяет существование бакета и создает его, если не существует"""
        try:
            async with self.create_client() as client:
                try:
                    await client.head_bucket(Bucket=self.bucket_name)
                except ClientError as e:
                    if e.response['Error']['Code'] == '404':
                        # Создаем бакет, если он не существует
                        await client.create_bucket(Bucket=self.bucket_name)
                        # Устанавливаем политику для публичного доступа к файлам
                        policy = {
                            "Version": "2012-10-17",
                            "Statement": [
                                {
                                    "Effect": "Allow",
                                    "Principal": {"AWS": "*"},
                                    "Action": ["s3:GetObject"],
                                    "Resource": [f"arn:aws:s3:::{self.bucket_name}/*"]
                                }
                            ]
                        }
                        await client.put_bucket_policy(
                            Bucket=self.bucket_name,
                            Policy=json.dumps(policy)
                        )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize storage: {str(e)}"
            )

    async def initialize(self) -> None:
        """Инициализирует хранилище"""
        await self._ensure_bucket_exists()

    async def upload_file(self, file: UploadFile, note_id: str) -> str:
        """
        Загружает файл в MinIO и возвращает URL для доступа к нему
        """
        try:
            # Создаем уникальное имя файла
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            # Убираем префикс notes/, так как это имя бакета
            object_name = f"{note_id}/{unique_filename}"

            # Читаем содержимое файла
            content = await file.read()

            async with self.create_client() as client:
                # Загружаем файл в MinIO
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=content,
                    ContentType=file.content_type
                )

                # Генерируем URL для доступа к файлу
                url = await client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': self.bucket_name,
                        'Key': object_name
                    },
                    ExpiresIn=7 * 24 * 3600  # 7 дней
                )

                return url

        except ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload file: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error during file upload: {str(e)}"
            )

    async def get_file(self, object_name: str) -> dict:
        """
        Получает файл из MinIO
        """
        try:
            async with self.create_client() as client:
                response = await client.get_object(
                    Bucket=self.bucket_name,
                    Key=object_name
                )
                return response
        except ClientError as e:
            raise HTTPException(
                status_code=404,
                detail=f"File not found: {str(e)}"
            )

    async def delete_file(self, object_name: str) -> None:
        """
        Удаляет файл из MinIO
        """
        try:
            async with self.create_client() as client:
                await client.delete_object(
                    Bucket=self.bucket_name,
                    Key=object_name
                )
        except ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete file: {str(e)}"
            )

    async def list_files(self, prefix: str = "") -> list:
        """
        Получает список файлов в бакете с указанным префиксом
        """
        try:
            async with self.create_client() as client:
                response = await client.list_objects_v2(
                    Bucket=self.bucket_name,
                    Prefix=prefix
                )
                return response.get('Contents', [])
        except ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to list files: {str(e)}"
            )


# Создаем глобальный экземпляр хранилища
storage = MinioStorage() 