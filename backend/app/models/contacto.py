from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Telefono(Base):
    __tablename__ = "telefono"

    id: Mapped[int] = mapped_column(primary_key=True)
    proveedor_id: Mapped[int | None] = mapped_column(ForeignKey("proveedor.id"))
    empleado_id: Mapped[int | None] = mapped_column(ForeignKey("empleado.id"))
    sucursal_id: Mapped[int | None] = mapped_column(ForeignKey("sucursal.id"))
    cliente_id: Mapped[int | None] = mapped_column(ForeignKey("cliente.id"))
    numero: Mapped[str] = mapped_column(String(20))


class Correo(Base):
    __tablename__ = "correo"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int | None] = mapped_column(ForeignKey("cliente.id"))
    sucursal_id: Mapped[int | None] = mapped_column(ForeignKey("sucursal.id"))
    empleado_id: Mapped[int | None] = mapped_column(ForeignKey("empleado.id"))
    proveedor_id: Mapped[int | None] = mapped_column(ForeignKey("proveedor.id"))
    correo: Mapped[str] = mapped_column(String(100))
