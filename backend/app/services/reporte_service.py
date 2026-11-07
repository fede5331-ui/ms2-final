# app/services/reporte_service.py
# Service de reportes: capa intermedia entre el router y el repository.
# Hoy solo reenvía los datos porque los reportes son de solo lectura
# y no tienen reglas de negocio. Tener esta capa permite agregar
# reglas después (por ejemplo, limitar un reporte a moderadores)
# sin tocar el router ni el SQL.

from app.repositories import reporte_repo


# ---------------------------------------------------------------
# Pedidos que recaudaron más que el promedio (consulta con subconsulta).
# ---------------------------------------------------------------
async def pedidos_sobre_el_promedio(conexion):
    return await reporte_repo.pedidos_sobre_el_promedio(conexion)


# ---------------------------------------------------------------
# Resumen de aportes por pedido (consulta con GROUP BY).
# ---------------------------------------------------------------
async def resumen_aportes_por_pedido(conexion):
    return await reporte_repo.resumen_aportes_por_pedido(conexion)