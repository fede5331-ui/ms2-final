import { useState } from 'react'
import { login, obtenerUsuario } from '../services/auth'
import { useNavigate } from 'react-router-dom'

function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

function validar() {
  if (!/^\S+@\S+\.\S+$/.test(email)) {
    return 'El email no tiene un formato válido'
  }
  if (!password) {
    return 'Ingresá la contraseña'
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
    const datos = await login(email, password)
    localStorage.setItem('token', datos.access_token)
    localStorage.setItem('rol', datos.rol)
    const usuario = await obtenerUsuario(datos.access_token)
    localStorage.setItem('usuario_id', usuario.id)
    navigate('/pedidos')
  } catch (err) {
    setError(err.message)
  }
}

  return (
    <div>
      <h1>Iniciar sesión</h1>
      <form onSubmit={manejarEnvio}>
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
        <button type="submit">Entrar</button>
      </form>
      {error && <p>{error}</p>}
    </div>
  )
}

export default Login