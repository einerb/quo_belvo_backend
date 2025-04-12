from fastapi import APIRouter
from fastapi import Depends

from app.api.v1.endpoints import auth, belvo
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/v1")

router.include_router(auth.router, tags=["Auth"])
router.include_router(belvo.router, tags=["Belvo API"], dependencies=[Depends(get_current_user)])