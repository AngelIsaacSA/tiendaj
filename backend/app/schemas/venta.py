from datetime import datetime

from pydantic import BaseModel, Field

from app.models.venta import METODOS_PAGO


class VentaCreate(BaseModel):
    cliente_id: int
    sucursal_id: int
    inventario_id: int
    cantidad: int = Field(gt=0)
    metodo_pago: str

    def validar_metodo_pago(self) -> None:
        if self.metodo_pago not in METODOS_PAGO:
            raise ValueError(f"metodo_pago debe ser uno de {METODOS_PAGO}")


class DetalleVentaOut(BaseModel):
    id: int
    videojuego_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float

    model_config = {"from_attributes": True}


class VentaOut(BaseModel):
    id: int
    cliente_id: int
    sucursal_id: int
    empleado_id: int
    total: float
    metodo_pago: str
    fecha_venta: datetime
    detalles: list[DetalleVentaOut] = []

    model_config = {"from_attributes": True}
