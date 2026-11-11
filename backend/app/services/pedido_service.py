from fastapi import HTTPException, status

from app.repositories import pedido_repo
from app.schemas.pedido import PedidoCrear
from pymysql.err import MySQLError


async def crear(conexion, usuario: dict, datos: PedidoCrear) -> dict:
    titulo = datos.titulo.strip()
    descripcion = datos.descripcion.strip()

    if len(titulo) < 5 or len(descripcion) < 10:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="El título y la descripción no pueden ser solo espacios",
        )

    nuevo_id = await pedido_repo.crear(
        conexion, usuario["id"], titulo, descripcion, datos.monto_objetivo
    )
    return await pedido_repo.buscar_por_id(conexion, nuevo_id)


async def listar(conexion, estado: str | None) -> list[dict]:
    return await pedido_repo.listar(conexion, estado)


async def obtener(conexion, pedido_id: int) -> dict:
    pedido = await pedido_repo.buscar_por_id(conexion, pedido_id)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El pedido no existe",
        )
    return pedido

# ---------------------------------------------------------------
# Cierra un pedido con su rendición de cuentas.
#   conexion:  conexión a MySQL (la entrega el router)
#   usuario:   dict del usuario logueado (id, nombre, email, rol)
#   pedido_id: pedido que se quiere cerrar
#   datos:     CierreCrear ya validado por Pydantic
# Devuelve el pedido actualizado (estado 'cerrado' + rendición).
# ---------------------------------------------------------------
async def cerrar(conexion, usuario: dict, pedido_id: int, datos):
    # Regla 1: el pedido tiene que existir; si no, 404.
    pedido = await pedido_repo.buscar_por_id(conexion, pedido_id)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El pedido no existe",
        )

    # Regla 2: solo el autor del pedido o un moderador pueden cerrarlo.
    # 403 = está logueado pero no tiene permiso para esta acción.
    es_autor = pedido["autor_id"] == usuario["id"]
    es_moderador = usuario["rol"] == "moderador"
    if not (es_autor or es_moderador):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el autor del pedido o un moderador pueden cerrarlo",
        )

    # Regla 3: no se puede cerrar un pedido que ya está cerrado (409).
    if pedido["estado"] == "cerrado":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El pedido ya está cerrado",
        )

    # Regla 4: la rendición no puede ser solo espacios en blanco.
    # Pydantic cuenta los espacios como caracteres, así que lo
    # revisamos acá después de limpiarlos con strip().
    rendicion = datos.rendicion.strip()
    if len(rendicion) < 10:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="La rendición es demasiado corta",
        )

    # Si pasó todas las reglas, cerramos. El repository devuelve cuántas
    # filas modificó: 0 significa que alguien lo cerró justo antes (409).
    filas = await pedido_repo.cerrar(conexion, pedido_id, rendicion)
    if filas == 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El pedido ya está cerrado",
        )

    # Devolvemos el pedido ya actualizado (con nombre del autor, etc.).
    return await pedido_repo.buscar_por_id(conexion, pedido_id)

# ---------------------------------------------------------------
# Edita un pedido existente.
#   conexion:  conexión a MySQL (la entrega el router)
#   usuario:   dict del usuario logueado (id, nombre, email, rol)
#   pedido_id: pedido que se quiere editar
#   datos:     PedidoActualizar ya validado por Pydantic
# Devuelve el pedido actualizado.
# ---------------------------------------------------------------
async def actualizar(conexion, usuario: dict, pedido_id: int, datos):
    # Regla 1: el pedido tiene que existir; si no, 404.
    pedido = await pedido_repo.buscar_por_id(conexion, pedido_id)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El pedido no existe",
        )

    # Regla 2: solo el autor del pedido o un moderador pueden editarlo.
    es_autor = pedido["autor_id"] == usuario["id"]
    es_moderador = usuario["rol"] == "moderador"
    if not (es_autor or es_moderador):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el autor del pedido o un moderador pueden editarlo",
        )

    # Regla 3: un pedido cerrado ya no se edita (su rendición es definitiva).
    if pedido["estado"] == "cerrado":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El pedido ya está cerrado",
        )

    # Regla 4: limpiamos espacios y evitamos textos que sean solo espacios
    # (Pydantic cuenta los espacios como caracteres, por eso lo revisamos acá).
    titulo = datos.titulo.strip()
    descripcion = datos.descripcion.strip()
    if len(titulo) < 5 or len(descripcion) < 10:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="El título o la descripción son demasiado cortos",
        )

    # Regla 5: el nuevo objetivo no puede ser menor a lo ya recaudado.
    # monto_recaudado llega de MySQL como Decimal y monto_objetivo como
    # float; no se pueden comparar directo (da error), por eso float().
    if datos.monto_objetivo < float(pedido["monto_recaudado"]):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="El monto objetivo no puede ser menor a lo ya recaudado",
        )

    # Si pasó todas las reglas, actualizamos y devolvemos el pedido
    # ya modificado (leído de nuevo, con nombre del autor, etc.).
    await pedido_repo.actualizar(conexion, pedido_id, titulo, descripcion, datos.monto_objetivo)
    return await pedido_repo.buscar_por_id(conexion, pedido_id)

# ---------------------------------------------------------------
# Borra un pedido (y sus novedades).
#   conexion:  conexión a MySQL (la entrega el router)
#   usuario:   dict del usuario logueado (id, nombre, email, rol)
#   pedido_id: pedido que se quiere borrar
# No devuelve nada: si no lanza error, se borró.
# ---------------------------------------------------------------
async def eliminar(conexion, usuario: dict, pedido_id: int):
    # Regla 1: el pedido tiene que existir; si no, 404.
    pedido = await pedido_repo.buscar_por_id(conexion, pedido_id)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El pedido no existe",
        )

    # Regla 2: solo el autor del pedido o un moderador pueden borrarlo.
    es_autor = pedido["autor_id"] == usuario["id"]
    es_moderador = usuario["rol"] == "moderador"
    if not (es_autor or es_moderador):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el autor del pedido o un moderador pueden borrarlo",
        )

    # Regla 3: un pedido cerrado no se borra, su rendición es parte
    # del historial y de la transparencia del sistema (409 Conflict).
    if pedido["estado"] == "cerrado":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un pedido cerrado no se puede borrar",
        )

    # Regla 4: un pedido con aportes no se borra: los aportes son dinero
    # registrado. La salida correcta es cerrarlo con su rendición.
    if await pedido_repo.contar_aportes(conexion, pedido_id) > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede borrar un pedido con aportes; cerralo con su rendición",
        )

    # Si pasó todas las reglas, borramos. Puede pasar que alguien registre
    # un aporte JUSTO entre el chequeo de arriba y el DELETE: en ese caso
    # MySQL rechaza el borrado con el error 1451 (clave foránea en uso) y
    # el repository ya hizo ROLLBACK. Lo traducimos a un 409 entendible.
    try:
        await pedido_repo.eliminar(conexion, pedido_id)
    except MySQLError as error:
        if error.args and error.args[0] == 1451:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede borrar un pedido con aportes; cerralo con su rendición",
            )
        raise   # cualquier otro error de MySQL se vuelve a lanzar tal cual