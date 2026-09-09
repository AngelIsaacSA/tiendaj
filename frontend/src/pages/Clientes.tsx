import { useEffect, useState, type FormEvent } from 'react'
import { api, ApiError } from '../api/client'
import type { Cliente, ClienteCreate } from '../api/types'

const initialForm: ClienteCreate = {
  nombre: '',
  apellido_paterno: '',
  apellido_materno: '',
  calle_id: 1,
}

export function Clientes() {
  const [clientes, setClientes] = useState<Cliente[]>([])
  const [form, setForm] = useState<ClienteCreate>(initialForm)
  const [error, setError] = useState<string | null>(null)

  function cargar() {
    api
      .get<Cliente[]>('/clientes')
      .then(setClientes)
      .catch(() => setError('No se pudo cargar la lista de clientes'))
  }

  useEffect(cargar, [])

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setError(null)
    try {
      await api.post<Cliente>('/clientes', { ...form, calle_id: Number(form.calle_id) })
      setForm(initialForm)
      cargar()
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Error al agregar')
    }
  }

  async function handleDelete(id: number) {
    await api.delete(`/clientes/${id}`)
    cargar()
  }

  return (
    <div>
      <h1>Clientes</h1>

      <form className="inline-form" onSubmit={handleSubmit}>
        <input
          placeholder="Nombre"
          value={form.nombre}
          onChange={(e) => setForm({ ...form, nombre: e.target.value })}
          required
        />
        <input
          placeholder="Apellido paterno"
          value={form.apellido_paterno}
          onChange={(e) => setForm({ ...form, apellido_paterno: e.target.value })}
          required
        />
        <input
          placeholder="Apellido materno"
          value={form.apellido_materno}
          onChange={(e) => setForm({ ...form, apellido_materno: e.target.value })}
        />
        <input
          type="number"
          placeholder="ID de calle"
          value={form.calle_id}
          onChange={(e) => setForm({ ...form, calle_id: Number(e.target.value) })}
          required
        />
        <button type="submit">Agregar</button>
      </form>

      {error && <p className="error">{error}</p>}

      <table>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Apellido paterno</th>
            <th>Apellido materno</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {clientes.map((cliente) => (
            <tr key={cliente.id}>
              <td>{cliente.nombre}</td>
              <td>{cliente.apellido_paterno}</td>
              <td>{cliente.apellido_materno}</td>
              <td>
                <button type="button" onClick={() => handleDelete(cliente.id)}>
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
