# app/repositories/reporte_repo.py
# Repository de reportes: contiene las consultas SQL de análisis.
# Como en los otros repositories, solo ejecuta SQL y devuelve datos;
# las reglas y el formato los resuelven las capas de arriba.

import aiomysql


# ---------------------------------------------------------------
# CONSULTA CON SUBCONSULTA
# Devuelve los pedidos que recaudaron MÁS que el promedio de todos.
#
# La consulta de adentro (SELECT AVG(monto_recaudado) FROM pedidos)
# se ejecuta primero y devuelve un único número: el promedio.
# La consulta de afuera usa ese número para filtrar con WHERE.
# El INNER JOIN con usuarios trae el nombre del autor.
# ---------------------------------------------------------------
async def pedidos_sobre_el_promedio(conexion):
    async with conexion.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(
            """
            SELECT p.id, p.titulo, p.estado, p.monto_objetivo,
                   p.monto_recaudado, u.nombre AS autor_nombre
            FROM pedidos p
            INNER JOIN usuarios u ON u.id = p.usuario_id
            WHERE p.monto_recaudado > (
                SELECT AVG(monto_recaudado) FROM pedidos
            )
            ORDER BY p.monto_recaudado DESC
            """
        )
        return await cursor.fetchall()


# ---------------------------------------------------------------
# CONSULTA CON GROUP BY
# Resumen por pedido: cuántos aportes recibió y cuánto sumaron.
#
# LEFT JOIN (en vez de INNER) para que aparezcan TAMBIÉN los pedidos
# sin aportes: con INNER JOIN desaparecerían del reporte.
# GROUP BY agrupa todas las filas de un mismo pedido en una sola.
# COUNT(a.id) cuenta los aportes del grupo (cuenta 0 si no hay).
# SUM(a.monto) suma sus montos; COALESCE lo pasa a 0 si es NULL.
# ---------------------------------------------------------------
async def resumen_aportes_por_pedido(conexion):
    async with conexion.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(
            """
            SELECT p.id, p.titulo, p.estado, p.monto_objetivo,
                   COUNT(a.id) AS cantidad_aportes,
                   COALESCE(SUM(a.monto), 0) AS total_aportado
            FROM pedidos p
            LEFT JOIN aportes a ON a.pedido_id = p.id
            GROUP BY p.id, p.titulo, p.estado, p.monto_objetivo
            ORDER BY total_aportado DESC, p.id
            """
        )
        return await cursor.fetchall()