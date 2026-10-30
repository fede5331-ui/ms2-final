import aiomysql
from app import config

pool = None


async def crear_pool():
    global pool
    pool = await aiomysql.create_pool(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        db=config.DB_NAME,
        charset="utf8mb4",
        autocommit=True,
        minsize=1,
        maxsize=10,
    )


async def cerrar_pool():
    pool.close()
    await pool.wait_closed()


async def obtener_conexion():
    async with pool.acquire() as conexion:
        yield conexion