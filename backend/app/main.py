from contextlib import asynccontextmanager
from fastapi import FastAPI
from app import database
from app.routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.crear_pool()
    yield
    await database.cerrar_pool()


app = FastAPI(title="Ayuda Animal API", lifespan=lifespan)

app.include_router(auth.router)


@app.get("/salud")
async def salud():
    async with database.pool.acquire() as conexion:
        async with conexion.cursor() as cursor:
            await cursor.execute("SELECT COUNT(*) FROM usuarios")
            (total,) = await cursor.fetchone()
    return {"estado": "ok", "usuarios": total}