from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.auth import get_current_user
from app.db import get_supabase
from app.services.claude import process_clip
from app.services.voyage import embed

router = APIRouter(prefix="/clips", tags=["clips"])


class ClipIn(BaseModel):
    url: str
    title: Optional[str] = None
    domain: Optional[str] = None
    favicon_url: Optional[str] = None
    raw_text: str


@router.post("", status_code=201)
def create_clip(payload: ClipIn, user_id: str = Depends(get_current_user)):
    extracted = process_clip(
        title=payload.title or "",
        raw_text=payload.raw_text,
        url=payload.url,
    )

    embedding = embed(payload.raw_text)

    result = get_supabase().table("clips").insert({
        "user_id":     user_id,
        "url":         payload.url,
        "title":       payload.title,
        "domain":      payload.domain,
        "favicon_url": payload.favicon_url,
        "raw_text":    payload.raw_text,
        "summary":     extracted["summary"],
        "entities":    extracted["entities"],
        "embedding":   embedding,
    }).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to save clip")

    return result.data[0]
