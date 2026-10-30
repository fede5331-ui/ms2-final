import aiomysql


async def buscar_por_email(conexion, email: str):
    async with conexion.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(
            "SELECT id, nombre, email, password_hash, rol "
            "FROM usuarios WHERE email = %s",
            (email,),
        )
        return await cursor.fetchone()


async def buscar_por_id(conexion, usuario_id: int):
    async with conexion.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(
            "SELECT id, nombre, email, rol FROM usuarios WHERE id = %s",
            (usuario_id,),
        )
        return await cursor.fetchone()


async def crear(conexion, nombre: str, email: str, password_hash: str) -> int:
    async with conexion.cursor() as cursor:
        await cursor.execute(
            "INSERT INTO usuarios (nombre, email, password_hash) "
            "VALUES (%s, %s, %s)",
            (nombre, email, password_hash),
        )
        return cursor.lastrowid