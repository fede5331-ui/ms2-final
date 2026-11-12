# Frontend - Sistema de Seguimiento de Pedidos de Ayuda Económica para la Protección Animal

Aplicación web en React (Vite, JavaScript) que consume la API del backend (FastAPI + MySQL).

## Requisitos

- Node.js y npm
- El backend corriendo en http://127.0.0.1:8000 (ver `backend/README.md`)

## Cómo levantarlo

1. Entrar a la carpeta del frontend:

```
cd frontend
```

2. Instalar las dependencias:

```
npm install
```

3. Levantar el servidor de desarrollo:

```
npm run dev
```

4. Abrir http://localhost:5173 en el navegador. El backend solo acepta ese origen (CORS), así que si Vite usa otro puerto hay que avisar para agregarlo.

## Estructura

- `src/pages`: pantallas (Login, Registro, Pedidos, Detalle, NuevoPedido, EditarPedido, Reportes)
- `src/components`: componentes compartidos (Menu)
- `src/services`: llamadas a la API (auth, pedidos, aportes, novedades, reportes)

## Pantallas

- `/login` y `/registro`: acceso con JWT, el token se guarda en localStorage
- `/pedidos`: listado con filtro por estado
- `/pedidos/:id`: detalle, aportes, novedades y cierre con rendición
- `/pedidos/nuevo` y `/pedidos/:id/editar`: alta y modificación
- `/reportes`: resumen por pedido, pedidos sobre el promedio y descarga en Excel

## Usuarios de prueba

Todos con la contraseña `Prueba123`:

- moderador@ayudaanimal.com (moderador)
- lucia@ejemplo.com, martin@ejemplo.com, carla@ejemplo.com (comunidad)