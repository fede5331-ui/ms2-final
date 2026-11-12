import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { crearPedido } from '../services/pedidos'
import { obtenerToken, cerrarSesion } from '../services/auth'

function NuevoPedido() {
  const [titulo, setTitulo] = useState('')
  const [descripcion, setDescripcion] = useState('')
  const [montoObjetivo, setMontoObjetivo] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const token = obtenerToken()

  function validar() {
    if (titulo.trim().length < 5 || titulo.trim().length > 150) {
      return 'El título debe tener entre 5 y 150 caracteres'
    }
    if (descripcion.trim().length < 10 || descripcion.trim().length > 5000) {
      return 'La descripción debe tener entre 10 y 5000 caracteres'
    }
    if (!montoObjetivo || Number(montoObjetivo) <= 0) {
      return 'El monto objetivo debe ser mayor a 0'
    }
    return ''
  }

  async function manejarEnvio(e) {
    e.preventDefault()
    const mensaje = validar()
    if (mensaje) {
      setError(mensaje)
      return
    }
    setError('')
    try {
      const pedido = await crearPedido(
        {
          titulo: titulo.trim(),
          descripcion: descripcion.trim(),
          monto_objetivo: Number(montoObjetivo),
        },
        token
      )
      navigate(`/pedidos/${pedido.id}`)
    } catch (err) {
      if (err.status === 401) {
        cerrarSesion()
        navigate('/login')
        return
      }
      setError(err.message)
    }
  }

  if (!token) {
    return (
      <p>
        <Link to="/login">Iniciá sesión</Link> para publicar un pedido
      </p>
    )
  }

  return (
    <div>
      <Link to="/pedidos">Volver al listado</Link>
      <h1>Nuevo pedido</h1>
      <form onSubmit={manejarEnvio}>
        <input
          type="text"
          placeholder="Título"
          value={titulo}
          onChange={(e) => setTitulo(e.target.value)}
        />
        <textarea
          placeholder="Descripción"
          value={descripcion}
          onChange={(e) => setDescripcion(e.target.value)}
        />
        <input
          type="number"
          placeholder="Monto objetivo"
          value={montoObjetivo}
          onChange={(e) => setMontoObjetivo(e.target.value)}
        />
        <button type="submit">Publicar</button>
      </form>
      {error && <p>{error}</p>}
    </div>
  )
}

export default NuevoPedido