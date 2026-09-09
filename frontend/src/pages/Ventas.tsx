import { useEffect, useState, type FormEvent } from 'react'
import { api, ApiError } from '../api/client'
import type { Cliente, MetodoPago, Venta, VentaCreate } from '../api/types'

const initialForm: VentaCreate = {
  cliente_id: 0,
  sucursal_id: 1,
  inventario_id: 0,
  cantidad: 1,
  metodo_pago: 'Efectivo',
}

const METODOS: MetodoPago[] = ['Efectivo', 'Tarjeta', 'Transferencia']

export function Ventas() {
  const [ventas, setVentas] = useState<Venta[]>([])
  const [clientes, setClientes] = useState<Cliente[]>([])
  const [form, setForm] = useState<VentaCreate>(initialForm)
  const [error, setError] = useState<string | null>(null)
  const [mensaje, setMensaje] = useState<string | null>(null)

  function cargar() {
    api
      .get<Venta[]>('/ventas')
      .then(setVentas)
      .catch(() => setError('No se pudo cargar el historial de ventas'))
  }

  useEffect(() => {
    cargar()
    api.get<Cliente[]>('/clientes').then(setClientes).catch(() => undefined)
  }, [])

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setError(null)
    setMensaje(null)
    try {
      const venta = await api.post<Venta>('/ventas', form)
      setMensaje(`Venta #${venta.id} registrada. Total: $${venta.total.toFixed(2)}`)
      setForm(initialForm)
      cargar()
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Error al registrar la venta')
    }
  }

  return (
    <div>
      <h1>Ventas</h1>

      <form className="inline-form" onSubmit={handleSubmit}>
        <select
          value={form.cliente_id}
          onChange={(e) => setForm({ ...form, cliente_id: Number(e.target.value) })}
          required
        >
          <option value={0} disabled>
            Cliente...
          </option>
          {clientes.map((c) => (
            <option key={c.id} value={c.id}>
              {c.nombre} {c.apellido_paterno}
            </option>
          ))}
        </select>
        <input
          type="number"
          placeholder="ID sucursal"
          value={form.sucursal_id}
          onChange={(e) => setForm({ ...form, sucursal_id: Number(e.target.value) })}
          required
        />
        <input
          type="number"
          placeholder="ID inventario"
          value={form.inventario_id || ''}
          onChange={(e) => setForm({ ...form, inventario_id: Number(e.target.value) })}
          required
        />
        <input
          type="number"
          min={1}
          placeholder="Cantidad"
          value={form.cantidad}
          onChange={(e) => setForm({ ...form, cantidad: Number(e.target.value) })}
          required
        />
        <select
          value={form.metodo_pago}
          onChange={(e) => setForm({ ...form, metodo_pago: e.target.value as MetodoPago })}
        >
          {METODOS.map((m) => (
            <option key={m} value={m}>
              {m}
            </option>
          ))}
        </select>
        <button type="submit">Registrar venta</button>
      </form>

      {error && <p className="error">{error}</p>}
      {mensaje && <p className="success">{mensaje}</p>}

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Cliente</th>
            <th>Total</th>
            <th>Método</th>
            <th>Fecha</th>
          </tr>
        </thead>
        <tbody>
          {ventas.map((venta) => (
            <tr key={venta.id}>
              <td>{venta.id}</td>
              <td>{venta.cliente_id}</td>
              <td>${venta.total.toFixed(2)}</td>
              <td>{venta.metodo_pago}</td>
              <td>{new Date(venta.fecha_venta).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
