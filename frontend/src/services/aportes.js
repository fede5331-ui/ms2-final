import { API_URL } from './config'

export async function obtenerAportes(pedidoId) {
  const respuesta = await fetch(`${API_URL}/pedidos/${pedidoId}/aportes`)
  const datos = await respuesta.json()
  if (!respuesta.ok) {
    throw new Error(
      typeof datos.detail === 'string' ? datos.detail : 'No se pudieron cargar los aportes'
    )
  }
  return datos
}

export async function crearAporte(pedidoId, monto, token) {
  const respuesta = await fetch(`${API_URL}/pedidos/${pedidoId}/aportes`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ monto }),
  })
  const datos = await respuesta.json()
  if (!respuesta.ok) {
    const error = new Error(
      typeof datos.detail === 'string' ? datos.detail : 'Revisá el monto ingresado'
    )
    error.status = respuesta.status
    throw error
  }
  return datos
}