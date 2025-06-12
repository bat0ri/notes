from typing import Optional, BinaryIO, AsyncGenerator
from contextlib import asynccontextmanager
from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from botocore.client import Config
from fastapi import UploadFile
import aiofiles
import os
from datetime import datetime, timedelta
import uuid
import json

from app.core.config import get_settings
from app.core.exceptions import StorageException, NotFoundException

settings = get_settings()


class MinioStorage:
    def __init__(self):
        self.config = {
            "aws_access_key_id": settings.MINIO_ROOT_USER,
            "aws_secret_access_key": settings.MINIO_ROOT_PASSWORD,
            "endpoint_url": f"http://{settings.MINIO_SERVER}:{settings.MINIO_PORT}",
            "region_name": "us-east-1",
            "config": Config(signature_version='s3v4')
        }
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self.session = get_session()

    @asynccontextmanager
    async def create_client(self) -> AsyncGenerator:
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def _ensure_bucket_exists(self) -> None:
        try:
            async with self.create_client() as client:
                try:
                    await client.head_bucket(Bucket=self.bucket_name)
                except ClientError as e:
                    if e.response['Error']['Code'] == '404':
                        await client.create_bucket(Bucket=self.bucket_name)
                    else:
                        raise StorageException(f"Ошибка при проверке бакета: {str(e)}")
        except Exception as e:
            raise StorageException(f"Не удалось инициализировать хранилище: {str(e)}")

    async def initialize(self) -> None:
        await self._ensure_bucket_exists()

    async def upload_file(self, file: UploadFile, object_name: str) -> None:
        try:
            async with self.create_client() as client:
                contents = await file.read()
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=contents,
                    ContentType=file.content_type
                )
        except Exception as e:
            raise StorageException(f"Не удалось загрузить файл: {str(e)}")

    async def get_file(self, object_name: str):
        try:
            async with self.create_client() as client:
                try:
                    response = await client.get_object(
                        Bucket=self.bucket_name,
                        Key=object_name
                    )
                    return response
                except ClientError as e:
                    if e.response['Error']['Code'] == 'NoSuchKey':
                        raise NotFoundException(f"Файл {object_name} не найден")
                    raise StorageException(f"Ошибка при получении файла: {str(e)}")
        except Exception as e:
            if isinstance(e, (NotFoundException, StorageException)):
                raise
            raise StorageException(f"Неожиданная ошибка при получении файла: {str(e)}")

    async def delete_file(self, object_name: str) -> None:
        try:
            async with self.create_client() as client:
                try:
                    await client.delete_object(
                        Bucket=self.bucket_name,
                        Key=object_name
                    )
                except ClientError as e:
                    if e.response['Error']['Code'] == 'NoSuchKey':
                        raise NotFoundException(f"Файл {object_name} не найден")
                    raise StorageException(f"Ошибка при удалении файла: {str(e)}")
        except Exception as e:
            if isinstance(e, (NotFoundException, StorageException)):
                raise
            raise StorageException(f"Неожиданная ошибка при удалении файла: {str(e)}")

    async def list_files(self, prefix: str = "") -> list:

        try:
            async with self.create_client() as client:
                try:
                    response = await client.list_objects_v2(
                        Bucket=self.bucket_name,
                        Prefix=prefix
                    )
                    return response.get('Contents', [])
                except ClientError as e:
                    raise StorageException(f"Ошибка при получении списка файлов: {str(e)}")
        except Exception as e:
            if isinstance(e, StorageException):
                raise
            raise StorageException(f"Неожиданная ошибка при получении списка файлов: {str(e)}")


storage = MinioStorage() 