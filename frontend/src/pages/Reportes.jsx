import { useState, useEffect } from 'react'
import {
  obtenerResumenPorPedido,
  obtenerPedidosSobrePromedio,
  descargarExcel,
} from '../services/reportes'

function Reportes() {
  const [resumen, setResumen] = useState([])
  const [sobrePromedio, setSobrePromedio] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    async function cargar() {
      try {
        setResumen(await obtenerResumenPorPedido())
        setSobrePromedio(await obtenerPedidosSobrePromedio())
        setError('')
      } catch (err) {
        setError(err.message)
      }
    }
    cargar()
  }, [])

  async function manejarDescarga() {
    try {
      await descargarExcel()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div>
      <h1>Reportes</h1>
      <button onClick={manejarDescarga}>Descargar Excel</button>
      {error && <p>{error}</p>}

      <h2>Resumen por pedido</h2>
      <table>
        <thead>
          <tr>
            <th>Título</th>
            <th>Estado</th>
            <th>Objetivo</th>
            <th>Cantidad de aportes</th>
            <th>Total aportado</th>
          </tr>
        </thead>
        <tbody>
          {resumen.map((r) => (
            <tr key={r.id}>
              <td>{r.titulo}</td>
              <td>{r.estado}</td>
              <td>${r.monto_objetivo.toLocaleString('es-AR')}</td>
              <td>{r.cantidad_aportes}</td>
              <td>${r.total_aportado.toLocaleString('es-AR')}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Pedidos que recaudaron más que el promedio</h2>
      {sobrePromedio.length === 0 ? (
        <p>Ningún pedido supera el promedio</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Título</th>
              <th>Autor</th>
              <th>Estado</th>
              <th>Objetivo</th>
              <th>Recaudado</th>
            </tr>
          </thead>
          <tbody>
            {sobrePromedio.map((p) => (
              <tr key={p.id}>
                <td>{p.titulo}</td>
                <td>{p.autor_nombre}</td>
                <td>{p.estado}</td>
                <td>${p.monto_objetivo.toLocaleString('es-AR')}</td>
                <td>${p.monto_recaudado.toLocaleString('es-AR')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default Reportes