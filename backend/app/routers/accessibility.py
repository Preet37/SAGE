from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.models import User
from app.security import get_current_user

router = APIRouter(prefix="/accessibility", tags=["accessibility"])


class A11yPrefs(BaseModel):
    dyslexia_font: bool = False
    high_contrast: bool = False
    reduce_motion: bool = False
    tts_voice: str = "default"


_PREFS: dict[int, A11yPrefs] = {}


@router.get("", response_model=A11yPrefs)
def get_prefs(user: User = Depends(get_current_user)):
    return _PREFS.get(user.id, A11yPrefs())


@router.put("", response_model=A11yPrefs)
def set_prefs(prefs: A11yPrefs, user: User = Depends(get_current_user)):
    _PREFS[user.id] = prefs
    return prefs
