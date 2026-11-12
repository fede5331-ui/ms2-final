import { API_URL } from './config'

export async function obtenerPedidos(estado) {
  const url = estado
    ? `${API_URL}/pedidos?estado=${estado}`
    : `${API_URL}/pedidos`
  const respuesta = await fetch(url)
  const datos = await respuesta.json()
  if (!respuesta.ok) {
    throw new Error(
      typeof datos.detail === 'string' ? datos.detail : 'No se pudieron cargar los pedidos'
    )
  }
  return datos
}

export async function obtenerPedido(id) {
  const respuesta = await fetch(`${API_URL}/pedidos/${id}`)
  const datos = await respuesta.json()
  if (!respuesta.ok) {
    throw new Error(
      typeof datos.detail === 'string' ? datos.detail : 'No se pudo cargar el pedido'
    )
  }
  return datos
}

export async function crearPedido(pedido, token) {
  const respuesta = await fetch(`${API_URL}/pedidos`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(pedido),
  })
  const datos = await respuesta.json()
  if (!respuesta.ok) {
    const error = new Error(
      typeof datos.detail === 'string' ? datos.detail : 'Revisá los datos ingresados'
    )
    error.status = respuesta.status
    throw error
  }
  return datos
}

export async function editarPedido(id, pedido, token) {
  const respuesta = await fetch(`${API_URL}/pedidos/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(pedido),
  })
  const datos = await respuesta.json()
  if (!respuesta.ok) {
    const error = new Error(
      typeof datos.detail === 'string' ? datos.detail : 'Revisá los datos ingresados'
    )
    error.status = respuesta.status
    throw error
  }
  return datos
}

export async function borrarPedido(id, token) {
  const respuesta = await fetch(`${API_URL}/pedidos/${id}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  })
  if (respuesta.status === 204) {
    return
  }
  const datos = await respuesta.json()
  const error = new Error(
    typeof datos.detail === 'string' ? datos.detail : 'No se pudo borrar el pedido'
  )
  error.status = respuesta.status
  throw error
}

export async function cerrarPedido(id, rendicion, token) {
  const respuesta = await fetch(`${API_URL}/pedidos/${id}/cierre`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ rendicion }),
  })
  const datos = await respuesta.json()
  if (!respuesta.ok) {
    const error = new Error(
      typeof datos.detail === 'string' ? datos.detail : 'Revisá la rendición ingresada'
    )
    error.status = respuesta.status
    throw error
  }
  return datos
}