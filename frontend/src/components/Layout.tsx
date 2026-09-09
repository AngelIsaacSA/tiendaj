import { NavLink, Outlet } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

export function Layout() {
  const { empleado, logout } = useAuth()

  return (
    <div className="app-shell">
      <header className="topbar">
        <span className="brand">TIENDAJ</span>
        <nav>
          <NavLink to="/" end>
            Dashboard
          </NavLink>
          <NavLink to="/videojuegos">Videojuegos</NavLink>
          <NavLink to="/clientes">Clientes</NavLink>
          <NavLink to="/ventas">Ventas</NavLink>
        </nav>
        <div className="user-info">
          {empleado && (
            <span>
              {empleado.nombre} · {empleado.puesto}
            </span>
          )}
          <button type="button" onClick={logout}>
            Salir
          </button>
        </div>
      </header>
      <main>
        <Outlet />
      </main>
    </div>
  )
}
