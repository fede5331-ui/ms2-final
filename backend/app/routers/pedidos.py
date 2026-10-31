from typing import Literal

from fastapi import APIRouter, Depends, status

from app.database import obtener_conexion
from app.dependencies import usuario_actual
from app.schemas.pedido import PedidoCrear, PedidoRespuesta
from app.services import pedido_service

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