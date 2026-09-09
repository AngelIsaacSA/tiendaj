export interface EmpleadoOut {
  id: number
  nombre: string
  apellido_paterno: string
  apellido_materno: string
  puesto: string
}

export interface Videojuego {
  id: number
  titulo: string
  precio: number
  clasificacion_id: string
  fecha_lanzamiento: string | null
}

export interface VideojuegoCreate {
  titulo: string
  precio: number
  clasificacion_id: string
  fecha_lanzamiento?: string | null
}

export interface Cliente {
  id: number
  nombre: string | null
  apellido_paterno: string | null
  apellido_materno: string | null
  calle_id: number
}

export interface ClienteCreate {
  nombre?: string
  apellido_paterno?: string
  apellido_materno?: string
  calle_id: number
}

export type MetodoPago = 'Efectivo' | 'Tarjeta' | 'Transferencia'

export interface VentaCreate {
  cliente_id: number
  sucursal_id: number
  inventario_id: number
  cantidad: number
  metodo_pago: MetodoPago
}

export interface DetalleVenta {
  id: number
  videojuego_id: number
  cantidad: number
  precio_unitario: number
  subtotal: number
}

export interface Venta {
  id: number
  cliente_id: number
  sucursal_id: number
  empleado_id: number
  total: number
  metodo_pago: string
  fecha_venta: string
  detalles: DetalleVenta[]
}

export interface DashboardStats {
  total_videojuegos: number
  total_clientes: number
  total_ventas: number
  ingresos: number
  ultimas_ventas: Venta[]
}
