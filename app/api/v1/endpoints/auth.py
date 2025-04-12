from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserCreate
from app.services.auth_service import create_user, authenticate_user
from app.core.security import create_access_token
from app.utils.response import success_response, error_response
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/auth")

@router.post("/register")
@limiter.limit("3/minute")
async def register(request: Request, user_data: UserCreate):
    try:
        user = await create_user(user_data)

        return success_response(
            data=user.model_dump(mode="json"),
            message="User successfully created!",
            status_code=201
        )

    except ValueError as e:
        return error_response(str(e), status_code=400)

    except Exception as e:
        return error_response(str(e), status_code=500)

@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        return error_response("Wrong credentials!",status_code=400)
    token = create_access_token({"sub": user.email, "username": user.username})
    
    return success_response(
        data={
            "access_token": token,
            "token_type": "bearer"
            },
        message="Token generated successfully!",
        status_code=200
    )
