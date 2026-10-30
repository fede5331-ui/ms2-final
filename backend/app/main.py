from contextlib import asynccontextmanager
from fastapi import FastAPI
from app import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.crear_pool()
    yield
    await database.cerrar_pool()


app = FastAPI(title="Ayuda Animal API", lifespan=lifespan)


@app.get("/salud")
async def salud():
    async with database.pool.acquire() as conexion:
        async with conexion.cursor() as cursor:
            await cursor.execute("SELECT COUNT(*) FROM usuarios")
            (total,) = await cursor.fetchone()
    return {"estado": "ok", "usuarios": total}