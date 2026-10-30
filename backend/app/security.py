from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app import config


def hashear_password(password: str) -> str:
    sal = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), sal).decode("utf-8")


def verificar_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"), password_hash.encode("utf-8")
    )


def crear_token(usuario_id: int, rol: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(
        minutes=config.JWT_EXPIRE_MINUTES
    )
    payload = {"sub": str(usuario_id), "rol": rol, "exp": expira}
    return jwt.encode(
        payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM
    )


def decodificar_token(token: str) -> dict:
    return jwt.decode(
        token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
    )