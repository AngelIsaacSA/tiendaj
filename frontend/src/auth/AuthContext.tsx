import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import { api, getToken, setToken as persistToken } from '../api/client'
import type { EmpleadoOut } from '../api/types'

interface AuthContextValue {
  empleado: EmpleadoOut | null
  isAuthenticated: boolean
  login: (rfc: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [empleado, setEmpleado] = useState<EmpleadoOut | null>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(() => getToken() !== null)

  useEffect(() => {
    if (getToken() && !empleado) {
      api
        .get<EmpleadoOut>('/auth/me')
        .then(setEmpleado)
        .catch(() => {
          persistToken(null)
          setIsAuthenticated(false)
        })
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  async function login(rfc: string, password: string) {
    const { access_token } = await api.post<{ access_token: string }>('/auth/login', {
      rfc,
      password,
    })
    persistToken(access_token)
    const me = await api.get<EmpleadoOut>('/auth/me')
    setEmpleado(me)
    setIsAuthenticated(true)
  }

  function logout() {
    persistToken(null)
    setEmpleado(null)
    setIsAuthenticated(false)
  }

  return (
    <AuthContext.Provider value={{ empleado, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth debe usarse dentro de AuthProvider')
  return ctx
}
