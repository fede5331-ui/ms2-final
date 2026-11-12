import { API_URL } from './config'

async function pedirJson(ruta, mensajeError) {
  const respuesta = await fetch(`${API_URL}${ruta}`)
  const datos = await respuesta.json()
  if (!respuesta.ok) {
    throw new Error(typeof datos.detail === 'string' ? datos.detail : mensajeError)
  }
  return datos
}

export function obtenerResumenPorPedido() {
  return pedirJson('/reportes/resumen-por-pedido', 'No se pudo cargar el resumen')
}

export function obtenerPedidosSobrePromedio() {
  return pedirJson('/reportes/pedidos-sobre-promedio', 'No se pudo cargar el reporte')
}

export async function descargarExcel() {
  const respuesta = await fetch(`${API_URL}/reportes/exportar/excel`)
  if (!respuesta.ok) {
    throw new Error('No se pudo generar el archivo')
  }
  const blob = await respuesta.blob()
  const url = URL.createObjectURL(blob)
  const enlace = document.createElement('a')
  enlace.href = url
  enlace.download = 'reportes_ayuda_animal.xlsx'
  enlace.click()
  URL.revokeObjectURL(url)
}