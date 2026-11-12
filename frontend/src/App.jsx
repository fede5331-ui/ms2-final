import { Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import Pedidos from './pages/Pedidos'
import Registro from './pages/Registro'
import Detalle from './pages/Detalle'
import NuevoPedido from './pages/NuevoPedido'
import Menu from './components/Menu'
import Reportes from './pages/Reportes'
import EditarPedido from './pages/EditarPedido'

function App() {
  return (
    <>
      <Menu />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/pedidos" element={<Pedidos />} />
        <Route path="/registro" element={<Registro />} />
        <Route path="/pedidos/:id" element={<Detalle />} />
        <Route path="/pedidos/nuevo" element={<NuevoPedido />} />
        <Route path="/reportes" element={<Reportes />} />
        <Route path="/pedidos/:id/editar" element={<EditarPedido />} />
      </Routes>
    </>
  )
}

export default App
