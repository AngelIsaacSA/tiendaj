from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.inventario import Videojuego


class Clasificacion(Base):
    __tablename__ = "clasificacion"

    id: Mapped[str] = mapped_column(String(5), primary_key=True)
    nombre: Mapped[str | None] = mapped_column(String(50))

    videojuegos: Mapped[list["Videojuego"]] = relationship(back_populates="clasificacion")


class Genero(Base):
    __tablename__ = "genero"

    id: Mapped[str] = mapped_column(String(5), primary_key=True)
    nombre: Mapped[str | None] = mapped_column(String(50))
