from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import logging

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_password_hash, verify_password
from app.db.session import get_db

logger = logging.getLogger(__name__)

async def create_user(user: UserCreate) -> UserResponse:
    async with get_db() as session:
        try:
            async with session.begin():
                hashed_password = get_password_hash(user.password)
                db_user = User(
                    username=user.username,
                    email=user.email,
                    password=hashed_password
                )
                session.add(db_user)
                await session.flush()
                await session.refresh(db_user)

            return UserResponse.model_validate(db_user)

        except IntegrityError:
            raise ValueError("E-mail or username already exists!")
        except Exception as e:
            logger.error(f"Error creando usuario: {str(e)}", exc_info=True)
            raise RuntimeError("Internal error")

async def authenticate_user(email: str, password: str):
    async with get_db() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if not user or not verify_password(password, user.password):
            return None
        return user