from datetime import datetime

from pydantic import BaseModel, Field


class PedidoCrear(BaseModel):
    titulo: str = Field(min_length=5, max_length=150)
    descripcion: str = Field(min_length=10, max_length=5000)
    monto_objetivo: float = Field(gt=0, le=99999999.99)


class PedidoRespuesta(BaseModel):
    id: int
    titulo: str
    descripcion: str
    monto_objetivo: float
    monto_recaudado: float
    estado: str
    autor_id: int
    autor_nombre: str
    rendicion: str | None = None
    cerrado_en: datetime | None = None
    creado_en: datetime

    # ---------------------------------------------------------------
# ENTRADA: lo que el frontend manda al EDITAR un pedido (PUT).
# Lleva los mismos tres campos y las mismas validaciones que al
# crearlo. El frontend manda siempre los tres (los valores nuevos,
# o los actuales si no cambió alguno); es lo habitual en un PUT.
# Ejemplo de body:
#   {"titulo": "Cirugía para Luna", "descripcion": "...", "monto_objetivo": 130000}
# ---------------------------------------------------------------
class PedidoActualizar(BaseModel):
    titulo: str = Field(min_length=5, max_length=150)
    descripcion: str = Field(min_length=10, max_length=5000)
    monto_objetivo: float = Field(gt=0, le=99999999.99)