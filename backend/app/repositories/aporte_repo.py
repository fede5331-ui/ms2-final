# app/repositories/aporte_repo.py
# Capa de acceso a datos de los aportes: acá vive el SQL.
# Esta capa no tiene reglas de negocio, solo habla con MySQL.

import aiomysql


async def registrar(conexion, pedido_id: int, usuario_id: int, monto: float) -> None:
    """Registra un aporte llamando al procedimiento almacenado.

    El procedimiento hace todo dentro de una transacción: inserta el aporte
    y suma el monto al total del pedido. Si algo falla, hace ROLLBACK y
    no queda nada a medias. Si todo sale bien, hace COMMIT.
    """
    async with conexion.cursor() as cursor:
        # CALL ejecuta un procedimiento almacenado. Los valores van como
        # parámetros (%s), nunca pegados en el texto, para evitar inyección SQL.
        await cursor.execute(
            "CALL sp_registrar_aporte(%s, %s, %s)",
            (pedido_id, usuario_id, monto),
        )


async def listar_por_pedido(conexion, pedido_id: int):
    """Devuelve los aportes de un pedido, del más nuevo al más viejo."""
    # DictCursor devuelve cada fila como diccionario (fila["monto"]).
    async with conexion.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(
            # INNER JOIN: une cada aporte con el usuario que lo hizo para
            # traer su nombre (u.nombre), que la tabla aportes no guarda.
            "SELECT a.id, a.pedido_id, a.usuario_id, "
            "       u.nombre AS usuario_nombre, a.monto, a.creado_en "
            "FROM aportes a "
            "INNER JOIN usuarios u ON u.id = a.usuario_id "
            "WHERE a.pedido_id = %s "
            "ORDER BY a.creado_en DESC, a.id DESC",
            (pedido_id,),
        )
        # fetchall devuelve la lista completa (vacía si no hay aportes).
        return await cursor.fetchall()