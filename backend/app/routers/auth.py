from fastapi import APIRouter, Depends, status

from app.database import obtener_conexion
from app.dependencies import usuario_actual
from app.schemas.usuario import (
    TokenRespuesta,
    UsuarioLogin,
    UsuarioRegistro,
    UsuarioRespuesta,
)
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post(
    "/registro",
    response_model=UsuarioRespuesta,
    status_code=status.HTTP_201_CREATED,
)
async def registro(datos: UsuarioRegistro, conexion=Depends(obtener_conexion)):
    return await auth_service.registrar(conexion, datos)


@router.post("/login", response_model=TokenRespuesta)
async def login(datos: UsuarioLogin, conexion=Depends(obtener_conexion)):
    return await auth_service.iniciar_sesion(conexion, datos)

@router.get("/me", response_model=UsuarioRespuesta)
async def yo(usuario=Depends(usuario_actual)):
    return usuario