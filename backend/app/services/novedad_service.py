# app/services/novedad_service.py
# Service de novedades: contiene las REGLAS DE NEGOCIO.
# No escribe SQL (eso es del repository) ni conoce rutas HTTP
# (eso es del router). Solo decide si una operación está permitida.

from fastapi import HTTPException, status

from app.repositories import novedad_repo, pedido_repo


# ---------------------------------------------------------------
# Publica una novedad en un pedido.
#   conexion: conexión a MySQL (la entrega el router)
#   usuario:  dict del usuario logueado (id, nombre, email, rol)
#   pedido_id: pedido donde se quiere publicar
#   datos:    NovedadCrear ya validado por Pydantic
# Devuelve la novedad creada (con el nombre del autor).
# ---------------------------------------------------------------
async def crear(conexion, usuario: dict, pedido_id: int, datos):
    # Regla 1: el pedido tiene que existir; si no, 404.
    pedido = await pedido_repo.buscar_por_id(conexion, pedido_id)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El pedido no existe",
        )

    # Regla 2: solo el autor del pedido o un moderador pueden publicar.
    # Si no cumple, 403 Forbidden (está logueado, pero no tiene permiso;
    # distinto de 401, que significa "no estás autenticado").
    es_autor = pedido["autor_id"] == usuario["id"]
    es_moderador = usuario["rol"] == "moderador"
    if not (es_autor or es_moderador):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el autor del pedido o un moderador pueden publicar novedades",
        )

    # Regla 3: un pedido cerrado ya no admite novedades; 409 Conflict.
    if pedido["estado"] == "cerrado":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El pedido ya está cerrado",
        )

    # Limpiamos espacios sobrantes y evitamos textos que sean solo espacios
    # (Pydantic cuenta los espacios como caracteres, por eso lo revisamos acá).
    texto = datos.texto.strip()
    if len(texto) < 5:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="El texto de la novedad es demasiado corto",
        )

    # Si pasó todas las reglas: insertamos y devolvemos la novedad completa.
    novedad_id = await novedad_repo.crear(conexion, pedido_id, usuario["id"], texto)
    return await novedad_repo.buscar_por_id(conexion, novedad_id)


# ---------------------------------------------------------------
# Lista las novedades de un pedido (público, no pide token).
# Si el pedido no existe devolvemos 404 en vez de una lista vacía,
# así el frontend distingue "sin novedades" de "pedido inexistente".
# ---------------------------------------------------------------
async def listar(conexion, pedido_id: int):
    pedido = await pedido_repo.buscar_por_id(conexion, pedido_id)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El pedido no existe",
        )
    return await novedad_repo.listar_por_pedido(conexion, pedido_id)