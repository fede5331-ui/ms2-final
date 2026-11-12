import { Link, useNavigate } from 'react-router-dom'
import { obtenerToken, cerrarSesion } from '../services/auth'

function Menu() {
  const navigate = useNavigate()
  const token = obtenerToken()

  function manejarSalida() {
    cerrarSesion()
    navigate('/login')
  }

  return (
    <nav>
      <Link to="/pedidos">Pedidos</Link>
      <Link to="/reportes">Reportes</Link>
      {token ? (
        <>
          <Link to="/pedidos/nuevo">Nuevo pedido</Link>
          <button onClick={manejarSalida}>Cerrar sesión</button>
        </>
      ) : (
        <>
          <Link to="/login">Iniciar sesión</Link>
          <Link to="/registro">Registrarme</Link>
        </>
      )}
    </nav>
  )
}

export default Menu