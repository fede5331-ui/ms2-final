import { API_URL } from './config'

function textoDeError(detail) {
  return typeof detail === 'string' ? detail : 'Revisá los datos ingresados'
}

export async function login(email, password) {
  const respuesta = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  const datos = await respuesta.json()
  if (!respuesta.ok) {
throw new Error(textoDeError(datos.detail))
  }
  return datos
}

export async function registrar(nombre, email, password) {
  const respuesta = await fetch(`${API_URL}/auth/registro`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre, email, password }),
  })
  const datos = await respuesta.json()
  if (!respuesta.ok) {
    throw new Error(textoDeError(datos.detail))
  }
  return datos
}

export function obtenerToken() {
  return localStorage.getItem('token')
}

export function cerrarSesion() {
  localStorage.removeItem('token')
  localStorage.removeItem('rol')
  localStorage.removeItem('usuario_id')
}

export async function obtenerUsuario(token) {
  const respuesta = await fetch(`${API_URL}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  const datos = await respuesta.json()
  if (!respuesta.ok) {
    throw new Error(textoDeError(datos.detail))
  }
  return datos
}

export function obtenerRol() {
  return localStorage.getItem('rol')
}

export function obtenerUsuarioId() {
  return Number(localStorage.getItem('usuario_id'))
}