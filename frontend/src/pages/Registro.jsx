import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { registrar } from '../services/auth'

function Registro() {
  const [nombre, setNombre] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  function validar() {
    if (nombre.trim().length < 2 || nombre.trim().length > 100) {
      return 'El nombre debe tener entre 2 y 100 caracteres'
    }
    if (!/^\S+@\S+\.\S+$/.test(email)) {
      return 'El email no tiene un formato válido'
    }
    if (password.length < 6) {
      return 'La contraseña debe tener al menos 6 caracteres'
    }
    if (new TextEncoder().encode(password).length > 72) {
      return 'La contraseña es demasiado larga'
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
      await registrar(nombre.trim(), email, password)
      navigate('/login')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div>
      <h1>Crear cuenta</h1>
      <form onSubmit={manejarEnvio}>
        <input
          type="text"
          placeholder="Nombre"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Registrarme</button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  )
}

export default Registro