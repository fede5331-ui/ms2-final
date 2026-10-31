# app/services/aporte_service.py
# Capa de servicios de los aportes: reglas de negocio y manejo de errores.

from fastapi import HTTPException, status
from pymysql.err import MySQLError

from app.repositories import aporte_repo, pedido_repo
from app.schemas.aporte import AporteCrear

# Código de error que MySQL devuelve cuando un procedimiento almacenado
# lanza un SIGNAL propio (por ejemplo "El pedido ya está cerrado").
CODIGO_SIGNAL = 1644


async def registrar(
    conexion, usuario: dict, pedido_id: int, datos: AporteCrear
) -> dict:
    """Registra un aporte y devuelve el pedido ya actualizado."""

    # Primera defensa: el pedido tiene que existir.
    pedido = await pedido_repo.buscar_por_id(conexion, pedido_id)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El pedido no existe",
        )

    # Segunda defensa: no se puede aportar a un pedido cerrado.
    # 409 (conflicto) = la petición es válida, pero choca con el estado actual.
    if pedido["estado"] == "cerrado":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El pedido ya está cerrado",
        )

    # Tercera defensa: el procedimiento almacenado vuelve a controlar todo
    # dentro de su transacción. Esto cubre el caso de que alguien cierre el
    # pedido justo entre nuestra consulta de arriba y esta llamada.
    try:
        await aporte_repo.registrar(
            conexion, pedido_id, usuario["id"], datos.monto
        )
    except MySQLError as error:
        # error.args = (código, mensaje). Si es un SIGNAL del procedimiento,
        # lo convertimos en un 409 con el mismo mensaje que escribimos en SQL.
        codigo = error.args[0] if error.args else None
        if codigo == CODIGO_SIGNAL:
            mensaje = error.args[1] if len(error.args) > 1 else "No se pudo registrar el aporte"
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=mensaje,
            )
        # Cualquier otro error es inesperado: lo dejamos subir (será un 500).
        raise

    # Devolvemos el pedido con el total ya sumado, para que el frontend
    # pueda refrescar la barra de progreso sin hacer otra petición.
    return await pedido_repo.buscar_por_id(conexion, pedido_id)


async def listar(conexion, pedido_id: int) -> list[dict]:
    """Devuelve los aportes de un pedido (404 si el pedido no existe)."""
    pedido = await pedido_repo.buscar_por_id(conexion, pedido_id)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El pedido no existe",
        )
    return await aporte_repo.listar_por_pedido(conexion, pedido_id)