import base64
import hashlib
from typing import Optional
from sqlalchemy.orm import Session

from app.models.image import Image


def generate_short_url(url: str, note_id: str) -> str:
    """
    Генерирует короткий URL для изображения.
    Использует комбинацию хеша URL и ID заметки для уникальности.
    """
    # Создаем хеш из URL и ID заметки
    hash_input = f"{url}:{note_id}".encode()
    hash_object = hashlib.md5(hash_input)
    # Берем первые 8 символов хеша и кодируем в base64
    short_hash = base64.urlsafe_b64encode(hash_object.digest()[:6]).decode('ascii')
    return short_hash


def get_unique_short_url(db: Session, url: str, note_id: str) -> str:
    """
    Генерирует уникальный короткий URL для изображения.
    Если URL уже существует, добавляет суффикс.
    """
    base_short_url = generate_short_url(url, note_id)
    short_url = base_short_url
    counter = 1
    
    # Проверяем существование URL и добавляем суффикс если нужно
    while db.query(Image).filter(Image.short_url == short_url).first() is not None:
        short_url = f"{base_short_url}_{counter}"
        counter += 1
    
    return short_url 