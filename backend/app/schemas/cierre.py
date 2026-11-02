# app/schemas/cierre.py
# Schema (molde de datos) de ENTRADA para cerrar un pedido.
# La respuesta no necesita un schema nuevo: al cerrar, devolvemos
# el pedido actualizado con PedidoRespuesta, que ya incluye
# estado, rendicion y cerrado_en.

from pydantic import BaseModel, Field


# ---------------------------------------------------------------
# Lo que el frontend manda al cerrar un pedido.
# Ejemplo de body:
#   {"rendicion": "Se gastaron $45000 en vacunas y $15000 en alimento."}
# ---------------------------------------------------------------
class CierreCrear(BaseModel):
    # La rendición es obligatoria: explica en qué se usó el dinero.
    # Pydantic devuelve 422 si falta, si tiene menos de 10 caracteres
    # o si supera los 5000 (validación del lado del servidor).
    rendicion: str = Field(min_length=10, max_length=5000)