# app/routers/novedades.py
# Router de novedades: define las URLs (endpoints) y conecta cada una
# con el service. No tiene reglas de negocio ni SQL: solo recibe la
# petición, llama al service y devuelve la respuesta.

from fastapi import APIRouter, Depends, status

from app.database import obtener_conexion
from app.dependencies import usuario_actual
from app.schemas.novedad import NovedadCrear, NovedadRespuesta
from app.services import novedad_service

# prefix: todas las rutas empiezan con /pedidos/{pedido_id}/novedades
# tags: agrupa las rutas en /docs bajo el título "Novedades"
router = APIRouter(prefix="/pedidos/{pedido_id}/novedades", tags=["Novedades"])


# ---------------------------------------------------------------
# POST /pedidos/{pedido_id}/novedades
# Publica una novedad. Requiere token (Depends(usuario_actual)):
# sin token o con token inválido responde 401 antes de llegar acá.
# status 201 = "creado". El response_model filtra lo que sale.
# ---------------------------------------------------------------
@router.post("", response_model=NovedadRespuesta, status_code=status.HTTP_201_CREATED)
async def publicar_novedad(
    pedido_id: int,                       # viene de la URL
    datos: NovedadCrear,                  # viene del body JSON, validado por Pydantic
    usuario: dict = Depends(usuario_actual),  # usuario logueado, sacado del token
    conexion=Depends(obtener_conexion),   # conexión a MySQL del pool
):
    return await novedad_service.crear(conexion, usuario, pedido_id, datos)


# ---------------------------------------------------------------
# GET /pedidos/{pedido_id}/novedades
# Lista las novedades de un pedido. Es público: no pide token,
# así cualquier visitante puede seguir cómo avanza el pedido.
# ---------------------------------------------------------------
@router.get("", response_model=list[NovedadRespuesta])
async def listar_novedades(
    pedido_id: int,
    conexion=Depends(obtener_conexion),
):
    return await novedad_service.listar(conexion, pedido_id)