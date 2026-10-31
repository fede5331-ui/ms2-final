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