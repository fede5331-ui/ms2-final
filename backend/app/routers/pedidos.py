from typing import Literal

from fastapi import APIRouter, Depends, status

from app.database import obtener_conexion
from app.dependencies import usuario_actual
from app.schemas.pedido import PedidoActualizar, PedidoCrear, PedidoRespuesta
from app.services import pedido_service

from app.schemas.cierre import CierreCrear

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post(
    "", response_model=PedidoRespuesta, status_code=status.HTTP_201_CREATED
)
async def crear_pedido(
    datos: PedidoCrear,
    usuario=Depends(usuario_actual),
    conexion=Depends(obtener_conexion),
):
    return await pedido_service.crear(conexion, usuario, datos)


@router.get("", response_model=list[PedidoRespuesta])
async def listar_pedidos(
    estado: Literal["abierto", "cerrado"] | None = None,
    conexion=Depends(obtener_conexion),
):
    return await pedido_service.listar(conexion, estado)


@router.get("/{pedido_id}", response_model=PedidoRespuesta)
async def ver_pedido(pedido_id: int, conexion=Depends(obtener_conexion)):
    return await pedido_service.obtener(conexion, pedido_id)

# ---------------------------------------------------------------
# POST /pedidos/{pedido_id}/cierre
# Cierra un pedido y registra su rendición de cuentas.
# Requiere token: Depends(usuario_actual) responde 401 si falta.
# Solo el autor o un moderador pueden cerrarlo (lo decide el service).
# Responde 200 con el pedido actualizado (estado, rendicion, cerrado_en).
# ---------------------------------------------------------------
@router.post("/{pedido_id}/cierre", response_model=PedidoRespuesta)
async def cerrar_pedido(
    pedido_id: int,                           # viene de la URL
    datos: CierreCrear,                       # body JSON con la rendición, validado
    usuario: dict = Depends(usuario_actual),  # usuario logueado, sacado del token
    conexion=Depends(obtener_conexion),       # conexión a MySQL del pool
):
    return await pedido_service.cerrar(conexion, usuario, pedido_id, datos)

# ---------------------------------------------------------------
# PUT /pedidos/{pedido_id}
# Edita título, descripción y monto objetivo de un pedido.
# Requiere token: sin él responde 401 antes de llegar acá.
# Solo el autor o un moderador pueden editarlo, y solo mientras
# esté abierto (lo decide el service). Responde 200 con el pedido
# actualizado.
# ---------------------------------------------------------------
@router.put("/{pedido_id}", response_model=PedidoRespuesta)
async def editar_pedido(
    pedido_id: int,                           # viene de la URL
    datos: PedidoActualizar,                  # body JSON con los valores nuevos, validado
    usuario: dict = Depends(usuario_actual),  # usuario logueado, sacado del token
    conexion=Depends(obtener_conexion),       # conexión a MySQL del pool
):
    return await pedido_service.actualizar(conexion, usuario, pedido_id, datos)

# ---------------------------------------------------------------
# DELETE /pedidos/{pedido_id}
# Borra un pedido y sus novedades.
# Requiere token: sin él responde 401 antes de llegar acá.
# Solo el autor o un moderador, y solo si el pedido está abierto y
# no tiene aportes (lo decide el service).
# Responde 204 (sin contenido): se borró y no hay nada para devolver.
# ---------------------------------------------------------------
@router.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
async def borrar_pedido(
    pedido_id: int,                           # viene de la URL
    usuario: dict = Depends(usuario_actual),  # usuario logueado, sacado del token
    conexion=Depends(obtener_conexion),       # conexión a MySQL del pool
):
    await pedido_service.eliminar(conexion, usuario, pedido_id)