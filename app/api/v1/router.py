from fastapi import APIRouter

from app.api.v1.endpoints import notes, tags

api_router = APIRouter()
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(tags.router, prefix="/tags", tags=["tags"]) 