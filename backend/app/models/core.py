from datetime import date

from sqlalchemy import Date, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Proveedor(Base):
    __tablename__ = "proveedor"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    rfc: Mapped[str | None] = mapped_column(String(13), unique=True)
    apellido_paterno: Mapped[str | None] = mapped_column(String(50))
    apellido_materno: Mapped[str | None] = mapped_column(String(50))


class Sucursal(Base):
    __tablename__ = "sucursal"

    id: Mapped[int] = mapped_column(primary_key=True)
    calle_id: Mapped[int] = mapped_column(ForeignKey("calle.id"))
    nombre: Mapped[str] = mapped_column(String(50))
    numero_exterior: Mapped[str] = mapped_column(String(10))
    numero_interior: Mapped[str | None] = mapped_column(String(10))

    inventarios: Mapped[list["Inventario"]] = relationship(back_populates="sucursal")  # noqa: F821


class Cliente(Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(primary_key=True)
    calle_id: Mapped[int] = mapped_column(ForeignKey("calle.id"))
    nombre: Mapped[str | None] = mapped_column(String(50))
    apellido_paterno: Mapped[str | None] = mapped_column(String(50))
    apellido_materno: Mapped[str | None] = mapped_column(String(50))
    fecha_registro: Mapped[date] = mapped_column(Date, server_default=func.current_date())


class Empleado(Base):
    __tablename__ = "empleado"

    id: Mapped[int] = mapped_column(primary_key=True)
    calle_id: Mapped[int] = mapped_column(ForeignKey("calle.id"))
    sucursal_id: Mapped[int] = mapped_column(ForeignKey("sucursal.id"))
    nombre: Mapped[str] = mapped_column(String(50))
    apellido_paterno: Mapped[str] = mapped_column(String(50))
    apellido_materno: Mapped[str] = mapped_column(String(50))
    curp: Mapped[str] = mapped_column(String(18), unique=True)
    rfc: Mapped[str] = mapped_column(String(13), unique=True)
    puesto: Mapped[str] = mapped_column(String(50))
    password_hash: Mapped[str | None] = mapped_column(String(255))
