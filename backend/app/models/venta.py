from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

METODOS_PAGO = ("Efectivo", "Tarjeta", "Transferencia")


class Venta(Base):
    __tablename__ = "venta"
    __table_args__ = (
        CheckConstraint(f"metodo_pago IN {METODOS_PAGO}", name="chk_metodo_pago"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    sucursal_id: Mapped[int] = mapped_column(ForeignKey("sucursal.id"))
    empleado_id: Mapped[int] = mapped_column(ForeignKey("empleado.id"))
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"))
    fecha_venta: Mapped[datetime] = mapped_column(server_default=func.now())
    total: Mapped[float] = mapped_column(Numeric(10, 2))
    metodo_pago: Mapped[str] = mapped_column()

    cliente: Mapped["Cliente"] = relationship()  # noqa: F821
    detalles: Mapped[list["DetalleVenta"]] = relationship(back_populates="venta")


class DetalleVenta(Base):
    __tablename__ = "detalle_venta"
    __table_args__ = (CheckConstraint("cantidad > 0", name="chk_cantidad_ven"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    venta_id: Mapped[int] = mapped_column(ForeignKey("venta.id"))
    videojuego_id: Mapped[int] = mapped_column(ForeignKey("videojuego.id"))
    cantidad: Mapped[int]
    precio_unitario: Mapped[float] = mapped_column(Numeric(10, 2))
    subtotal: Mapped[float] = mapped_column(Numeric(10, 2))

    venta: Mapped["Venta"] = relationship(back_populates="detalles")
    videojuego: Mapped["Videojuego"] = relationship()  # noqa: F821
