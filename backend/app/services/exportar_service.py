# app/services/exportar_service.py
# Service de exportación: arma el archivo Excel (.xlsx) con los
# reportes. No escribe SQL: reutiliza reporte_service, que ya
# trae los datos. No conoce HTTP: solo devuelve los bytes del archivo.

from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Font

from app.services import reporte_service


# ---------------------------------------------------------------
# Escribe una hoja de Excel.
#   hoja:       la hoja (worksheet) donde se escribe
#   encabezados: lista con los títulos de las columnas
#   filas:      lista de listas con los valores de cada fila
# Pone los encabezados en negrita y ajusta el ancho de cada columna.
# ---------------------------------------------------------------
def _escribir_hoja(hoja, encabezados, filas):
    # Primera fila: los títulos de las columnas
    hoja.append(encabezados)
    for celda in hoja[1]:
        celda.font = Font(bold=True)

    # Una fila de Excel por cada registro del reporte
    for fila in filas:
        hoja.append(fila)

    # Ancho de cada columna = el texto más largo de esa columna + 2
    for columna in hoja.columns:
        ancho = max(len(str(celda.value)) if celda.value is not None else 0 for celda in columna)
        hoja.column_dimensions[columna[0].column_letter].width = ancho + 2


# ---------------------------------------------------------------
# Genera el libro de Excel completo con los dos reportes y
# devuelve su contenido en bytes (listo para enviar como descarga).
#   Hoja 1: resumen de aportes por pedido (consulta con GROUP BY)
#   Hoja 2: pedidos sobre el promedio (consulta con subconsulta)
# ---------------------------------------------------------------
async def generar_excel(conexion) -> bytes:
    # Traemos los datos de los dos reportes
    resumen = await reporte_service.resumen_aportes_por_pedido(conexion)
    sobre_promedio = await reporte_service.pedidos_sobre_el_promedio(conexion)

    libro = Workbook()

    # Hoja 1: el libro ya trae una hoja vacía, la reutilizamos
    hoja1 = libro.active
    hoja1.title = "Resumen por pedido"
    _escribir_hoja(
        hoja1,
        ["ID", "Título", "Estado", "Monto objetivo", "Cantidad de aportes", "Total aportado"],
        [
            [r["id"], r["titulo"], r["estado"], float(r["monto_objetivo"]),
             r["cantidad_aportes"], float(r["total_aportado"])]
            for r in resumen
        ],
    )

    # Hoja 2: creamos una hoja nueva para el segundo reporte
    hoja2 = libro.create_sheet("Sobre el promedio")
    _escribir_hoja(
        hoja2,
        ["ID", "Título", "Estado", "Monto objetivo", "Monto recaudado", "Autor"],
        [
            [p["id"], p["titulo"], p["estado"], float(p["monto_objetivo"]),
             float(p["monto_recaudado"]), p["autor_nombre"]]
            for p in sobre_promedio
        ],
    )

    # Guardamos el libro en memoria (BytesIO) en vez de en un archivo
    # del disco, y devolvemos sus bytes.
    memoria = BytesIO()
    libro.save(memoria)
    return memoria.getvalue()