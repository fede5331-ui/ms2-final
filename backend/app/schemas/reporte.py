# app/schemas/reporte.py
# Schemas (moldes) de SALIDA de los reportes.
# Estos reportes solo se leen, así que no hay schemas de entrada.
# Los montos son float para que el JSON los lleve como números
# (si fueran Decimal, Pydantic los serializaría como texto).

from pydantic import BaseModel


# ---------------------------------------------------------------
# Una fila del reporte "pedidos sobre el promedio"
# (resultado de la consulta con subconsulta).
# ---------------------------------------------------------------
class PedidoSobrePromedio(BaseModel):
    id: int
    titulo: str
    estado: str
    monto_objetivo: float
    monto_recaudado: float
    autor_nombre: str


# ---------------------------------------------------------------
# Una fila del reporte "resumen de aportes por pedido"
# (resultado de la consulta con GROUP BY).
# cantidad_aportes viene de COUNT y total_aportado de SUM.
# ---------------------------------------------------------------
class ResumenPedido(BaseModel):
    id: int
    titulo: str
    estado: str
    monto_objetivo: float
    cantidad_aportes: int
    total_aportado: float