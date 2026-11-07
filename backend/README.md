# Backend: Sistema de Seguimiento de Pedidos de Ayuda Económica para la Protección Animal

API en **FastAPI** con **MySQL** (SQL escrito a mano, driver asíncrono `aiomysql`, sin ORM) y autenticación con **JWT**.
Metodología de Sistemas II, UTN. Entrega: 10/11/2026.

## Arquitectura en capas

```
router (HTTP)  ->  service (reglas de negocio)  ->  repository (SQL)  ->  MySQL
```

- `app/routers/`: define las URLs y recibe/devuelve JSON.
- `app/services/`: reglas de negocio (permisos, estados, validaciones).
- `app/repositories/`: único lugar donde se escribe SQL (consultas parametrizadas).
- `app/schemas/`: moldes de datos y validaciones de entrada/salida (Pydantic).
- `app/security.py` y `app/dependencies.py`: hash de contraseñas, JWT y usuario logueado.
- `sql/`: `schema.sql` (tablas y procedimiento almacenado) y `datos_prueba.sql`.

## Cómo levantarlo

1. Tener **Python 3.13** y **MySQL 8** instalados.
2. Desde la carpeta `backend`, crear y activar el entorno virtual:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Crear un archivo `.env` en `backend/` (no se sube a Git) con estas variables:
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=tu_contraseña
   DB_NAME=ayuda_animal
   JWT_SECRET=una_clave_larga_y_secreta
   JWT_ALGORITHM=HS256
   JWT_EXPIRE_MINUTES=60
   ```
4. En DBeaver, ejecutar como script (Alt+X), en este orden: `sql/schema.sql` y después `sql/datos_prueba.sql` (una sola vez).
5. Levantar el servidor:
   ```powershell
   uvicorn app.main:app --reload
   ```
6. Abrir http://127.0.0.1:8000/docs para ver y probar todas las rutas.

## Usuarios de prueba

Todos con la contraseña `Prueba123`:

| Email | Rol |
| --- | --- |
| moderador@ayudaanimal.com | moderador |
| lucia@ejemplo.com | comunidad |
| martin@ejemplo.com | comunidad |
| carla@ejemplo.com | comunidad |

## Rutas principales

| Método | Ruta | Quién |
| --- | --- | --- |
| POST | `/auth/registro`, `/auth/login` | Cualquiera |
| GET | `/auth/me` | Con token |
| POST | `/pedidos` | Con token |
| GET | `/pedidos`, `/pedidos/{id}` | Cualquiera |
| POST | `/pedidos/{id}/aportes` | Con token |
| GET | `/pedidos/{id}/aportes`, `/pedidos/{id}/novedades` | Cualquiera |
| POST | `/pedidos/{id}/novedades`, `/pedidos/{id}/cierre` | Autor del pedido o moderador |
| GET | `/reportes/resumen-por-pedido`, `/reportes/pedidos-sobre-promedio` | Cualquiera |
| GET | `/reportes/exportar/excel` | Cualquiera |

## Requisitos de la consigna y dónde están

- **Tablas normalizadas (4):** `sql/schema.sql` (`usuarios`, `pedidos`, `aportes`, `novedades`).
- **Procedimiento almacenado con COMMIT/ROLLBACK:** `sp_registrar_aporte`, en `sql/schema.sql`; se llama desde `app/repositories/aporte_repo.py`.
- **Consultas:** INNER JOIN en `pedido_repo.py`, subconsulta y GROUP BY en `reporte_repo.py`.
- **JWT y roles:** `app/security.py`, `app/dependencies.py` y los services.
- **Validación en servidor:** schemas de Pydantic y reglas de los services.
- **Reportes exportables:** Excel en `app/services/exportar_service.py`.