import { useEffect, useState } from 'react'
import { api } from '../api/client'
import type { DashboardStats } from '../api/types'

export function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api
      .get<DashboardStats>('/dashboard')
      .then(setStats)
      .catch(() => setError('No se pudo cargar el dashboard'))
  }, [])

  if (error) return <p className="error">{error}</p>
  if (!stats) return <p>Cargando...</p>

  return (
    <div>
      <h1>Dashboard</h1>
      <div className="stat-grid">
        <div className="stat-card">
          <span className="stat-value">{stats.total_videojuegos}</span>
          <span className="stat-label">Videojuegos</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{stats.total_clientes}</span>
          <span className="stat-label">Clientes</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{stats.total_ventas}</span>
          <span className="stat-label">Ventas</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">${stats.ingresos.toFixed(2)}</span>
          <span className="stat-label">Ingresos</span>
        </div>
      </div>

      <h2>Últimas ventas</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Total</th>
            <th>Método</th>
            <th>Fecha</th>
          </tr>
        </thead>
        <tbody>
          {stats.ultimas_ventas.map((venta) => (
            <tr key={venta.id}>
              <td>{venta.id}</td>
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
