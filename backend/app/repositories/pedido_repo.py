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