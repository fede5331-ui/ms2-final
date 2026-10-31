# app/routers/aportes.py
# Capa de rutas de los aportes: recibe las peticiones HTTP y las pasa al
# servicio. No tiene lógica propia.

from fastapi import APIRouter, Depends, status

from app.database import obtener_conexion
from app.dependencies import usuario_actual
from app.schemas.aporte import AporteCrear, AporteRespuesta
from app.schemas.pedido import PedidoRespuesta
from app.services import aporte_service

# El prefijo incluye {pedido_id}: todas las rutas de este archivo cuelgan
# de un pedido concreto, por ejemplo /pedidos/2/aportes.
router = APIRouter(prefix="/pedidos/{pedido_id}/aportes", tags=["Aportes"])


@router.post(
    "", response_model=PedidoRespuesta, status_code=status.HTTP_201_CREATED
)
async def registrar_aporte(
    pedido_id: int,  # viene de la URL
    datos: AporteCrear,  # viene del cuerpo JSON: {"monto": ...}
    usuario=Depends(usuario_actual),  # exige token; es quien aporta
    conexion=Depends(obtener_conexion),  # conexión del pool
):
    """Registra un aporte y devuelve el pedido con el total actualizado."""
    return await aporte_service.registrar(conexion, usuario, pedido_id, datos)


@router.get("", response_model=list[AporteRespuesta])
async def listar_aportes(
    pedido_id: int,  # viene de la URL
    conexion=Depends(obtener_conexion),  # ruta pública: no pide token
):
    """Lista los aportes de un pedido, del más nuevo al más viejo."""
    return await aporte_service.listar(conexion, pedido_id)