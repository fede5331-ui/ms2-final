import aiomysql

CONSULTA_PEDIDOS = """
    SELECT p.id, p.titulo, p.descripcion, p.monto_objetivo,
           p.monto_recaudado, p.estado, p.rendicion, p.cerrado_en,
           p.creado_en, u.id AS autor_id, u.nombre AS autor_nombre
    FROM pedidos p
    INNER JOIN usuarios u ON u.id = p.usuario_id
"""


async def listar(conexion, estado: str | None = None):
    sql = CONSULTA_PEDIDOS
    parametros = ()
    if estado is not None:
        sql += " WHERE p.estado = %s"
        parametros = (estado,)
    sql += " ORDER BY p.creado_en DESC, p.id DESC"

    async with conexion.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(sql, parametros)
        return await cursor.fetchall()


async def buscar_por_id(conexion, pedido_id: int):
    async with conexion.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(CONSULTA_PEDIDOS + " WHERE p.id = %s", (pedido_id,))
        return await cursor.fetchone()


async def crear(
    conexion, usuario_id: int, titulo: str, descripcion: str, monto_objetivo: float
) -> int:
    async with conexion.cursor() as cursor:
        await cursor.execute(
            "INSERT INTO pedidos (usuario_id, titulo, descripcion, monto_objetivo) "
            "VALUES (%s, %s, %s, %s)",
            (usuario_id, titulo, descripcion, monto_objetivo),
        )
        return cursor.lastrowid

    # ---------------------------------------------------------------
# Cierra un pedido: cambia su estado a 'cerrado', guarda la
# rendición y registra la fecha/hora del cierre (cerrado_en).
#
# La condición "AND estado = 'abierto'" es una protección extra:
# si dos personas intentan cerrar a la vez, solo una modifica la
# fila; la otra afecta 0 filas. Así nunca se cierra dos veces.
#
# Devuelve la cantidad de filas modificadas (1 = se cerró,
# 0 = ya estaba cerrado o no existe).
# ---------------------------------------------------------------
async def cerrar(conexion, pedido_id: int, rendicion: str) -> int:
    async with conexion.cursor() as cursor:
        await cursor.execute(
            "UPDATE pedidos "
            "SET estado = 'cerrado', rendicion = %s, cerrado_en = NOW() "
            "WHERE id = %s AND estado = 'abierto'",
            (rendicion, pedido_id),
        )
        # rowcount = cuántas filas modificó el UPDATE
        return cursor.rowcount

    # ---------------------------------------------------------------
# Edita un pedido: cambia título, descripción y monto objetivo.
#
# "AND estado = 'abierto'" es una protección extra: aunque el
# service ya verificó que el pedido está abierto, si alguien lo
# cerró justo en ese instante este UPDATE no modifica nada.
#
# No devuelve cuántas filas cambió, a propósito: en MySQL el rowcount
# cuenta solo las filas que CAMBIARON de verdad. Si el usuario guarda
# los mismos valores que ya tenía, daría 0 y parecería un error
# cuando no lo es. El service vuelve a leer el pedido para devolverlo.
# ---------------------------------------------------------------
async def actualizar(conexion, pedido_id: int, titulo: str, descripcion: str, monto_objetivo: float) -> None:
    async with conexion.cursor() as cursor:
        await cursor.execute(
            "UPDATE pedidos "
            "SET titulo = %s, descripcion = %s, monto_objetivo = %s "
            "WHERE id = %s AND estado = 'abierto'",
            (titulo, descripcion, monto_objetivo, pedido_id),
        )