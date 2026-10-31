# app/schemas/aporte.py
# Esquemas (validación) del módulo de aportes: definen qué datos entran
# y qué datos salen de la API para los aportes.

from datetime import datetime

from pydantic import BaseModel, Field


class AporteCrear(BaseModel):
    """Datos que envía el frontend para registrar un aporte.

    Solo se manda el monto: el pedido sale de la URL y quién aporta
    sale del token, así nadie puede aportar a nombre de otro.
    """

    # Monto en pesos. Debe ser mayor a 0 (gt=0) y entrar en un DECIMAL(10,2).
    monto: float = Field(gt=0, le=99999999.99)


class AporteRespuesta(BaseModel):
    """Un aporte tal como lo devuelve la API en el listado."""

    id: int
    pedido_id: int
    usuario_id: int
    # Nombre de quien aportó. Viene del INNER JOIN con la tabla usuarios.
    usuario_nombre: str
    monto: float
    # Fecha y hora del aporte (hora del servidor, sin zona horaria).
    creado_en: datetime