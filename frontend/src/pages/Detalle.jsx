import { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { obtenerPedido, borrarPedido, cerrarPedido } from "../services/pedidos";
import { obtenerAportes, crearAporte } from "../services/aportes";
import { obtenerNovedades, crearNovedad } from "../services/novedades";
import {
  obtenerToken,
  cerrarSesion,
  obtenerRol,
  obtenerUsuarioId,
} from "../services/auth";

function Detalle() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [pedido, setPedido] = useState(null);
  const [aportes, setAportes] = useState([]);
  const [novedades, setNovedades] = useState([]);
  const [error, setError] = useState("");
  const [monto, setMonto] = useState("");
  const [errorAporte, setErrorAporte] = useState("");
  const [errorAccion, setErrorAccion] = useState("");
  const [texto, setTexto] = useState("");
  const [errorNovedad, setErrorNovedad] = useState("");
  const [rendicion, setRendicion] = useState("");
  const [errorCierre, setErrorCierre] = useState("");
  const token = obtenerToken();

  useEffect(() => {
    async function cargar() {
      try {
        const datosPedido = await obtenerPedido(id);
        const datosAportes = await obtenerAportes(id);
        const datosNovedades = await obtenerNovedades(id);
        setPedido(datosPedido);
        setAportes(datosAportes);
        setNovedades(datosNovedades);
        setError("");
      } catch (err) {
        setError(err.message);
      }
    }
    cargar();
  }, [id]);

  function sesionVencida(err) {
    if (err.status === 401) {
      cerrarSesion();
      navigate("/login");
      return true;
    }
    return false;
  }

  async function manejarAporte(e) {
    e.preventDefault();
    if (!monto || Number(monto) <= 0) {
      setErrorAporte("El monto debe ser mayor a 0");
      return;
    }
    try {
      const pedidoActualizado = await crearAporte(id, Number(monto), token);
      setPedido(pedidoActualizado);
      setAportes(await obtenerAportes(id));
      setMonto("");
      setErrorAporte("");
    } catch (err) {
      if (sesionVencida(err)) return;
      setErrorAporte(err.message);
    }
  }

  async function manejarBorrado() {
    if (!window.confirm("¿Seguro que querés borrar este pedido?")) {
      return;
    }
    try {
      await borrarPedido(id, token);
      navigate("/pedidos");
    } catch (err) {
      if (sesionVencida(err)) return;
      setErrorAccion(err.message);
    }
  }

  async function manejarNovedad(e) {
    e.preventDefault();
    if (texto.trim().length < 5 || texto.trim().length > 2000) {
      setErrorNovedad("La novedad debe tener entre 5 y 2000 caracteres");
      return;
    }
    try {
      await crearNovedad(id, texto.trim(), token);
      setNovedades(await obtenerNovedades(id));
      setTexto("");
      setErrorNovedad("");
    } catch (err) {
      if (sesionVencida(err)) return;
      setErrorNovedad(err.message);
    }
  }

  async function manejarCierre(e) {
    e.preventDefault();
    if (rendicion.trim().length < 10 || rendicion.trim().length > 5000) {
      setErrorCierre("La rendición debe tener entre 10 y 5000 caracteres");
      return;
    }
    if (
      !window.confirm(
        "Un pedido cerrado no se puede reabrir. ¿Cerrar el pedido?",
      )
    ) {
      return;
    }
    try {
      const pedidoCerrado = await cerrarPedido(id, rendicion.trim(), token);
      setPedido(pedidoCerrado);
      setRendicion("");
      setErrorCierre("");
    } catch (err) {
      if (sesionVencida(err)) return;
      setErrorCierre(err.message);
    }
  }

  if (error) {
    return (
      <div>
        <p className="error">{error}</p>
        <Link to="/pedidos">Volver al listado</Link>
      </div>
    );
  }

  if (!pedido) {
    return <p>Cargando...</p>;
  }

  const puedeModificar =
    token &&
    pedido.estado === "abierto" &&
    (pedido.autor_id === obtenerUsuarioId() || obtenerRol() === "moderador");

  return (
    <div>
      <Link to="/pedidos">Volver al listado</Link>
      <h1>{pedido.titulo}</h1>
      <p>{pedido.descripcion}</p>
      <p>Publicado por: {pedido.autor_nombre}</p>
      <p>Fecha: {new Date(pedido.creado_en).toLocaleDateString("es-AR")}</p>
      <p>Objetivo: ${pedido.monto_objetivo.toLocaleString("es-AR")}</p>
      <p>Recaudado: ${pedido.monto_recaudado.toLocaleString("es-AR")}</p>
      <p>
        Estado: {pedido.estado}
        {pedido.monto_recaudado >= pedido.monto_objetivo && (
          <span className="meta">Meta lograda</span>
        )}
      </p>
      {pedido.rendicion && (
        <div>
          <h2>Rendición</h2>
          <p>{pedido.rendicion}</p>
        </div>
      )}

      {puedeModificar && (
        <div>
          <Link to={`/pedidos/${pedido.id}/editar`}>Editar</Link>
          <button onClick={manejarBorrado}>Borrar</button>
          {errorAccion && <p className="error">{errorAccion}</p>}
        </div>
      )}

      <h2>Aportes</h2>
      {aportes.length === 0 ? (
        <p>Todavía no hay aportes</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Quién</th>
              <th>Monto</th>
              <th>Fecha</th>
            </tr>
          </thead>
          <tbody>
            {aportes.map((a) => (
              <tr key={a.id}>
                <td>{a.usuario_nombre}</td>
                <td>${a.monto.toLocaleString("es-AR")}</td>
                <td>{new Date(a.creado_en).toLocaleDateString("es-AR")}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {pedido.estado === "abierto" &&
        (token ? (
          <form onSubmit={manejarAporte}>
            <input
              type="number"
              placeholder="Monto a aportar"
              value={monto}
              onChange={(e) => setMonto(e.target.value)}
            />
            <button type="submit">Aportar</button>
            {errorAporte && <p className="error">{errorAporte}</p>}
          </form>
        ) : (
          <p>
            <Link to="/login">Iniciá sesión</Link> para aportar
          </p>
        ))}

      <h2>Novedades</h2>
      {novedades.length === 0 ? (
        <p>Todavía no hay novedades</p>
      ) : (
        <ul>
          {novedades.map((n) => (
            <li key={n.id}>
              <strong>{n.usuario_nombre}</strong> (
              {new Date(n.creado_en).toLocaleDateString("es-AR")}): {n.texto}
            </li>
          ))}
        </ul>
      )}

      {puedeModificar && (
        <form onSubmit={manejarNovedad}>
          <textarea
            placeholder="Escribí una novedad"
            value={texto}
            onChange={(e) => setTexto(e.target.value)}
          />
          <button type="submit">Publicar novedad</button>
          {errorNovedad && <p className="error">{errorNovedad}</p>}
        </form>
      )}

      {puedeModificar && (
        <form onSubmit={manejarCierre}>
          <h2>Cerrar pedido</h2>
          <textarea
            placeholder="Rendición: en qué se usó el dinero"
            value={rendicion}
            onChange={(e) => setRendicion(e.target.value)}
          />
          <button type="submit">Cerrar con rendición</button>
          {errorCierre && <p className="error">{errorCierre}</p>}
        </form>
      )}
    </div>
  );
}

export default Detalle;
