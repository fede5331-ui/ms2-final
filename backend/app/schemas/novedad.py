# app/schemas/novedad.py
# Schemas (moldes de datos) del módulo de novedades.
# Un schema define qué forma tienen los datos que ENTRAN a la API
# (lo que manda el frontend) y los que SALEN (lo que le devolvemos).

from datetime import datetime

from pydantic import BaseModel, Field


# ---------------------------------------------------------------
# ENTRADA: lo que el frontend manda al publicar una novedad.
# Ejemplo de body: {"texto": "Ya llevamos a la perra al veterinario"}
# ---------------------------------------------------------------
class NovedadCrear(BaseModel):
    # El texto es obligatorio. Pydantic rechaza (422) si tiene
    # menos de 5 caracteres o más de 2000. Esa es la validación
    # del lado del servidor que pide la consigna.
    texto: str = Field(min_length=5, max_length=2000)


# ---------------------------------------------------------------
# SALIDA: lo que la API devuelve por cada novedad.
# usuario_nombre no está en la tabla novedades: lo traeremos
# con un INNER JOIN a usuarios (igual que hicimos en aportes).
# ---------------------------------------------------------------
class NovedadRespuesta(BaseModel):
    id: int
    pedido_id: int
    usuario_id: int
    usuario_nombre: str
    texto: str
    creado_en: datetime