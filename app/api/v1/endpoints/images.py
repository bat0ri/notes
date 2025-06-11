from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from app.api import deps
from app.schemas.image import Image
from app.services.image import ImageService

router = APIRouter()


@router.post("/notes/{note_id}/images", response_model=Image)
async def upload_image(
    note_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    image_service: ImageService = Depends(deps.get_image_service)
) -> Image:
    """
    Загружает изображение для заметки.
    """
    return await image_service.upload_image(db=db, note_id=note_id, file=file)


@router.get("/notes/{note_id}/images", response_model=List[Image])
def get_note_images(
    note_id: str,
    db: Session = Depends(deps.get_db),
    image_service: ImageService = Depends(deps.get_image_service)
) -> List[Image]:
    """
    Получает все изображения для заметки.
    """
    return image_service.get_by_note(db=db, note_id=note_id)


@router.delete("/images/{image_id}")
async def delete_image(
    image_id: str,
    db: Session = Depends(deps.get_db),
    image_service: ImageService = Depends(deps.get_image_service)
) -> dict:
    """
    Удаляет изображение.
    """
    await image_service.delete_image(db=db, image_id=image_id)
    return {"status": "success"}


@router.get("/i/{short_url}")
async def get_image_by_short_url(
    short_url: str,
    db: Session = Depends(deps.get_db),
    image_service: ImageService = Depends(deps.get_image_service)
):
    """
    Получение изображения по короткому URL.
    Перенаправляет на полный URL изображения.
    """
    image = image_service.get_by_short_url(db=db, short_url=short_url)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return RedirectResponse(url=image.url) 