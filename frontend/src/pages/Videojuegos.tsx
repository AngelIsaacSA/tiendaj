import { useEffect, useState, type FormEvent } from 'react'
import { api, ApiError } from '../api/client'
import type { Videojuego, VideojuegoCreate } from '../api/types'

const initialForm: VideojuegoCreate = {
  titulo: '',
  precio: 0,
  clasificacion_id: '',
  fecha_lanzamiento: '',
}

export function Videojuegos() {
  const [juegos, setJuegos] = useState<Videojuego[]>([])
  const [form, setForm] = useState<VideojuegoCreate>(initialForm)
  const [error, setError] = useState<string | null>(null)

  function cargar() {
    api
      .get<Videojuego[]>('/videojuegos')
      .then(setJuegos)
      .catch(() => setError('No se pudo cargar el catálogo'))
  }

  useEffect(cargar, [])

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setError(null)
    try {
      await api.post<Videojuego>('/videojuegos', {
        ...form,
        precio: Number(form.precio),
        fecha_lanzamiento: form.fecha_lanzamiento || null,
      })
      setForm(initialForm)
      cargar()
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Error al agregar')
    }
  }

  async function handleDelete(id: number) {
    await api.delete(`/videojuegos/${id}`)
    cargar()
  }

  return (
    <div>
      <h1>Videojuegos</h1>

      <form className="inline-form" onSubmit={handleSubmit}>
        <input
          placeholder="Título"
          value={form.titulo}
          onChange={(e) => setForm({ ...form, titulo: e.target.value })}
          required
        />
        <input
          type="number"
          step="0.01"
          placeholder="Precio"
          value={form.precio || ''}
          onChange={(e) => setForm({ ...form, precio: Number(e.target.value) })}
          required
        />
        <input
          placeholder="Clasificación (ej. E, M)"
          value={form.clasificacion_id}
          onChange={(e) => setForm({ ...form, clasificacion_id: e.target.value })}
          required
        />
        <input
          type="date"
          value={form.fecha_lanzamiento ?? ''}
          onChange={(e) => setForm({ ...form, fecha_lanzamiento: e.target.value })}
        />
        <button type="submit">Agregar</button>
      </form>

      {error && <p className="error">{error}</p>}

      <table>
        <thead>
          <tr>
            <th>Título</th>
            <th>Precio</th>
            <th>Clasificación</th>
            <th>Lanzamiento</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {juegos.map((juego) => (
            <tr key={juego.id}>
              <td>{juego.titulo}</td>
              <td>${juego.precio.toFixed(2)}</td>
              <td>{juego.clasificacion_id}</td>
              <td>{juego.fecha_lanzamiento ?? '-'}</td>
              <td>
                <button type="button" onClick={() => handleDelete(juego.id)}>
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
