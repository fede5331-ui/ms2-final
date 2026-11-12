import { API_URL } from './config'

export async function obtenerNovedades(pedidoId) {
  const respuesta = await fetch(`${API_URL}/pedidos/${pedidoId}/novedades`)
  const datos = await respuesta.json()
  if (!respuesta.ok) {
    throw new Error(
      typeof datos.detail === 'string' ? datos.detail : 'No se pudieron cargar las novedades'
    )
  }
  return datos
}

export async function crearNovedad(pedidoId, texto, token) {
  const respuesta = await fetch(`${API_URL}/pedidos/${pedidoId}/novedades`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ texto }),
  })
  const datos = await respuesta.json()
  if (!respuesta.ok) {
    const error = new Error(
      typeof datos.detail === 'string' ? datos.detail : 'Revisá el texto ingresado'
    )
    error.status = respuesta.status
    throw error
  }
  return datos
}