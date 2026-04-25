from fastapi import APIRouter, Depends

from app.models import User
from app.security import get_current_user

router = APIRouter(prefix="/network", tags=["network"])


@router.get("/peers")
def peers(_: User = Depends(get_current_user)):
    return {"peers": []}
