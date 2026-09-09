from pydantic import BaseModel

from app.schemas.venta import VentaOut


class DashboardStats(BaseModel):
    total_videojuegos: int
    total_clientes: int
    total_ventas: int
    ingresos: float
    ultimas_ventas: list[VentaOut]
