from fastapi import HTTPException, status

from app.repositories import pedido_repo
from app.schemas.pedido import PedidoCrear


async def crear(conexion, usuario: dict, datos: PedidoCrear) -> dict:
    titulo = datos.titulo.strip()
    descripcion = datos.descripcion.strip()

    if len(titulo) < 5 or len(descripcion) < 10:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="El título y la descripción no pueden ser solo espacios",
        )

    nuevo_id = await pedido_repo.crear(
        conexion, usuario["id"], titulo, descripcion, datos.monto_objetivo
    )
    return await pedido_repo.buscar_por_id(conexion, nuevo_id)


async def listar(conexion, estado: str | None) -> list[dict]:
    return await pedido_repo.listar(conexion, estado)


async def obtener(conexion, pedido_id: int) -> dict:
    pedido = await pedido_repo.buscar_por_id(conexion, pedido_id)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El pedido no existe",
        )
    return pedido