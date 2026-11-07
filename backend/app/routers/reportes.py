# app/routers/reportes.py
# Router de reportes: define las URLs de los reportes y las conecta
# con el service. No tiene SQL ni reglas de negocio.

from fastapi import APIRouter, Depends, Response

from app.database import obtener_conexion
from app.schemas.reporte import PedidoSobrePromedio, ResumenPedido
from app.services import reporte_service
from app.services import exportar_service

# prefix: todas las rutas empiezan con /reportes
# tags: las agrupa en /docs bajo el título "Reportes"
router = APIRouter(prefix="/reportes", tags=["Reportes"])


# ---------------------------------------------------------------
# GET /reportes/pedidos-sobre-promedio
# Pedidos que recaudaron más que el promedio (subconsulta).
# Público: no pide token.
# ---------------------------------------------------------------
@router.get("/pedidos-sobre-promedio", response_model=list[PedidoSobrePromedio])
async def pedidos_sobre_promedio(conexion=Depends(obtener_conexion)):
    return await reporte_service.pedidos_sobre_el_promedio(conexion)


# ---------------------------------------------------------------
# GET /reportes/resumen-por-pedido
# Cantidad de aportes y total aportado por pedido (GROUP BY).
# Público: no pide token.
# ---------------------------------------------------------------
@router.get("/resumen-por-pedido", response_model=list[ResumenPedido])
async def resumen_por_pedido(conexion=Depends(obtener_conexion)):
    return await reporte_service.resumen_aportes_por_pedido(conexion)

# ---------------------------------------------------------------
# GET /reportes/exportar/excel
# Descarga un archivo Excel (.xlsx) con los dos reportes.
# Público, como los demás reportes.
#
# Devolvemos Response (no JSON) con los bytes del archivo:
#  - media_type: el tipo oficial de los archivos .xlsx, para que el
#    navegador sepa que es una planilla de Excel.
#  - Content-Disposition: attachment le indica al navegador que lo
#    DESCARGUE (en vez de mostrarlo) y le pone el nombre del archivo.
# ---------------------------------------------------------------
@router.get("/exportar/excel")
async def exportar_excel(conexion=Depends(obtener_conexion)):
    contenido = await exportar_service.generar_excel(conexion)
    return Response(
        content=contenido,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="reportes_ayuda_animal.xlsx"'},
    )