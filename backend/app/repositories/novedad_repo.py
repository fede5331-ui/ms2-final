# app/repositories/novedad_repo.py
# Repository de novedades: la ÚNICA capa que escribe SQL para la
# tabla novedades. No decide reglas de negocio (eso lo hace el service),
# solo ejecuta consultas y devuelve datos.


# ---------------------------------------------------------------
# Consulta base: trae las novedades junto con el nombre del autor.
# INNER JOIN une cada novedad (n) con su usuario (u) usando
# usuario_id, así obtenemos u.nombre sin hacer otra consulta.
# La guardamos en una constante para reutilizarla.
# ---------------------------------------------------------------

# aiomysql: lo necesitamos para pedir el cursor tipo DictCursor
import aiomysql

CONSULTA_NOVEDADES = """
    SELECT n.id, n.pedido_id, n.usuario_id,
           u.nombre AS usuario_nombre,
           n.texto, n.creado_en
    FROM novedades n
    INNER JOIN usuarios u ON u.id = n.usuario_id
"""


# ---------------------------------------------------------------
# Inserta una novedad nueva y devuelve el id que MySQL le asignó.
# Los %s son parámetros: el driver los reemplaza de forma segura,
# lo que protege contra SQL injection (nunca armamos el SQL
# pegando texto del usuario a mano).
# ---------------------------------------------------------------
async def crear(conexion, pedido_id: int, usuario_id: int, texto: str) -> int:
    async with conexion.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(
            "INSERT INTO novedades (pedido_id, usuario_id, texto) "
            "VALUES (%s, %s, %s)",
            (pedido_id, usuario_id, texto),
        )
        # lastrowid = el id autoincremental de la fila recién insertada
        return cursor.lastrowid


# ---------------------------------------------------------------
# Busca UNA novedad por su id (la usamos para devolver la novedad
# completa, con nombre de autor, después de crearla).
# Devuelve un dict, o None si no existe.
# ---------------------------------------------------------------
async def buscar_por_id(conexion, novedad_id: int):
    async with conexion.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(CONSULTA_NOVEDADES + " WHERE n.id = %s", (novedad_id,))
        return await cursor.fetchone()


# ---------------------------------------------------------------
# Lista todas las novedades de un pedido, la más nueva primero.
# El id como segundo criterio desempata si dos tienen la misma hora.
# ---------------------------------------------------------------
async def listar_por_pedido(conexion, pedido_id: int):
    async with conexion.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(
            CONSULTA_NOVEDADES
            + " WHERE n.pedido_id = %s ORDER BY n.creado_en DESC, n.id DESC",
            (pedido_id,),
        )
        return await cursor.fetchall()