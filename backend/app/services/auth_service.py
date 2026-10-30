from fastapi import HTTPException, status

from app import security
from app.repositories import usuario_repo
from app.schemas.usuario import UsuarioLogin, UsuarioRegistro


async def registrar(conexion, datos: UsuarioRegistro) -> dict:
    existente = await usuario_repo.buscar_por_email(conexion, datos.email)
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El email ya está registrado",
        )

    password_hash = security.hashear_password(datos.password)
    nuevo_id = await usuario_repo.crear(
        conexion, datos.nombre, datos.email, password_hash
    )
    return await usuario_repo.buscar_por_id(conexion, nuevo_id)


async def iniciar_sesion(conexion, datos: UsuarioLogin) -> dict:
    usuario = await usuario_repo.buscar_por_email(conexion, datos.email)

    if not usuario or not security.verificar_password(
        datos.password, usuario["password_hash"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )

    token = security.crear_token(usuario["id"], usuario["rol"])
    return {"access_token": token, "token_type": "bearer", "rol": usuario["rol"]}