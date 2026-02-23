from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.entities import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_email = payload.get("sub")
    except JWTError as exc:
        raise credentials_exception from exc

    if not user_email:
        raise credentials_exception

    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise credentials_exception
    return user


def require_roles(*allowed_roles: str):
    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Недостаточно прав")
        return user

    return checker
