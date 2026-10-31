import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app import security
from app.database import obtener_conexion
from app.repositories import usuario_repo

esquema_bearer = HTTPBearer(auto_error=False)


def _no_autorizado(detalle: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detalle,
        headers={"WWW-Authenticate": "Bearer"},
    )


async def usuario_actual(
    credenciales: HTTPAuthorizationCredentials | None = Depends(esquema_bearer),
    conexion=Depends(obtener_conexion),
) -> dict:
    if credenciales is None:
        raise _no_autorizado("Falta el token de autenticación")

    try:
        datos = security.decodificar_token(credenciales.credentials)
    except jwt.ExpiredSignatureError:
        raise _no_autorizado("El token venció, volvé a iniciar sesión")
    except jwt.InvalidTokenError:
        raise _no_autorizado("Token inválido")

    usuario = await usuario_repo.buscar_por_id(conexion, int(datos["sub"]))
    if usuario is None:
        raise _no_autorizado("El usuario del token ya no existe")

    return usuario