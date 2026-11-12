import { useState, useEffect } from "react";
import { obtenerPedidos } from "../services/pedidos";
import { Link } from "react-router-dom";

function Pedidos() {
  const [pedidos, setPedidos] = useState([]);
  const [estado, setEstado] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    async function cargar() {
      try {
        const datos = await obtenerPedidos(estado);
        setPedidos(datos);
        setError("");
      } catch (err) {
        setError(err.message);
      }
    }
    cargar();
  }, [estado]);

  return (
    <div>
      <h1>Pedidos</h1>
      <select value={estado} onChange={(e) => setEstado(e.target.value)}>
        <option value="">Todos</option>
        <option value="abierto">Abiertos</option>
        <option value="cerrado">Cerrados</option>
      </select>
      {error && <p>{error}</p>}
      <table>
        <thead>
          <tr>
            <th>Título</th>
            <th>Autor</th>
            <th>Objetivo</th>
            <th>Recaudado</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          {pedidos.map((p) => (
            <tr key={p.id}>
              <td>
                <Link to={`/pedidos/${p.id}`}>{p.titulo}</Link>
              </td>
              <td>{p.autor_nombre}</td>
              <td>${p.monto_objetivo.toLocaleString("es-AR")}</td>
              <td>${p.monto_recaudado.toLocaleString("es-AR")}</td>
              <td>
                {p.estado}
                {p.monto_recaudado >= p.monto_objetivo && (
                  <span className="meta">Meta lograda</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Pedidos;
