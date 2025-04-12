from fastapi import Depends
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from app.utils.exceptions import CustomHTTPException

from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise CustomHTTPException("Invalid token!", status_code=401)

        return payload
    except JWTError:
        raise CustomHTTPException("Invalid token!", status_code=401)