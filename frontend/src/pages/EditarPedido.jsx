import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { obtenerPedido, editarPedido } from '../services/pedidos'
import { obtenerToken, cerrarSesion } from '../services/auth'

function EditarPedido() {
  const { id } = useParams()
  const navigate = useNavigate()
  const token = obtenerToken()
  const [titulo, setTitulo] = useState('')
  const [descripcion, setDescripcion] = useState('')
  const [montoObjetivo, setMontoObjetivo] = useState('')
  const [montoRecaudado, setMontoRecaudado] = useState(0)
  const [cargado, setCargado] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    async function cargar() {
      try {
        const pedido = await obtenerPedido(id)
        setTitulo(pedido.titulo)
        setDescripcion(pedido.descripcion)
        setMontoObjetivo(pedido.monto_objetivo)
        setMontoRecaudado(pedido.monto_recaudado)
        setCargado(true)
      } catch (err) {
        setError(err.message)
      }
    }
    cargar()
  }, [id])

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
    if (Number(montoObjetivo) < montoRecaudado) {
      return 'El monto objetivo no puede ser menor a lo ya recaudado'
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
      await editarPedido(
        id,
        {
          titulo: titulo.trim(),
          descripcion: descripcion.trim(),
          monto_objetivo: Number(montoObjetivo),
        },
        token
      )
      navigate(`/pedidos/${id}`)
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
        <Link to="/login">Iniciá sesión</Link> para editar un pedido
      </p>
    )
  }

  if (!cargado) {
    return (
      <div>
        {error ? <p className="error">{error}</p> : <p>Cargando...</p>}
        <Link to="/pedidos">Volver al listado</Link>
      </div>
    )
  }

  return (
    <div>
      <Link to={`/pedidos/${id}`}>Volver al detalle</Link>
      <h1>Editar pedido</h1>
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
        <button type="submit">Guardar cambios</button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  )
}

export default EditarPedido