from datetime import date

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Videojuego(Base):
    __tablename__ = "videojuego"
    __table_args__ = (CheckConstraint("precio > 0", name="chk_precio_vid"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    clasificacion_id: Mapped[str] = mapped_column(ForeignKey("clasificacion.id"))
    titulo: Mapped[str] = mapped_column(String(150))
    precio: Mapped[float] = mapped_column(Numeric(10, 2))
    fecha_lanzamiento: Mapped[date | None]

    clasificacion: Mapped["Clasificacion"] = relationship(back_populates="videojuegos")  # noqa: F821
    plataformas: Mapped[list["Plataforma"]] = relationship(back_populates="videojuego")


class Plataforma(Base):
    __tablename__ = "plataforma"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    videojuego_id: Mapped[int] = mapped_column(ForeignKey("videojuego.id"))
    nombre: Mapped[str | None] = mapped_column(String(50))

    videojuego: Mapped["Videojuego"] = relationship(back_populates="plataformas")
    inventarios: Mapped[list["Inventario"]] = relationship(back_populates="plataforma")


class Inventario(Base):
    __tablename__ = "inventario"
    __table_args__ = (CheckConstraint("stock >= 0", name="chk_stock_min"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    plataforma_id: Mapped[str] = mapped_column(ForeignKey("plataforma.id"))
    sucursal_id: Mapped[int] = mapped_column(ForeignKey("sucursal.id"))
    nombre: Mapped[str | None] = mapped_column(String(50))
    stock: Mapped[int]

    plataforma: Mapped["Plataforma"] = relationship(back_populates="inventarios")
    sucursal: Mapped["Sucursal"] = relationship(back_populates="inventarios")  # noqa: F821
