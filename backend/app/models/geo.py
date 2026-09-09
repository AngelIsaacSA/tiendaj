from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Pais(Base):
    __tablename__ = "pais"

    id: Mapped[str] = mapped_column(String(6), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))

    estados: Mapped[list["Estado"]] = relationship(back_populates="pais")


class Estado(Base):
    __tablename__ = "estado"

    id: Mapped[str] = mapped_column(String(6), primary_key=True)
    pais_id: Mapped[str] = mapped_column(ForeignKey("pais.id"))
    nombre: Mapped[str] = mapped_column(String(50))

    pais: Mapped["Pais"] = relationship(back_populates="estados")
    ciudades: Mapped[list["Ciudad"]] = relationship(back_populates="estado")


class Ciudad(Base):
    __tablename__ = "ciudad"

    id: Mapped[int] = mapped_column(primary_key=True)
    estado_id: Mapped[str] = mapped_column(ForeignKey("estado.id"))
    nombre: Mapped[str] = mapped_column(String(50))

    estado: Mapped["Estado"] = relationship(back_populates="ciudades")
    colonias: Mapped[list["Colonia"]] = relationship(back_populates="ciudad")


class Colonia(Base):
    __tablename__ = "colonia"

    id: Mapped[str] = mapped_column(String(10), primary_key=True)
    ciudad_id: Mapped[int] = mapped_column(ForeignKey("ciudad.id"))
    nombre: Mapped[str] = mapped_column(String(50))

    ciudad: Mapped["Ciudad"] = relationship(back_populates="colonias")
    calles: Mapped[list["Calle"]] = relationship(back_populates="colonia")


class Calle(Base):
    __tablename__ = "calle"

    id: Mapped[int] = mapped_column(primary_key=True)
    colonia_id: Mapped[str] = mapped_column(ForeignKey("colonia.id"))
    nombre: Mapped[str] = mapped_column(String(100))

    colonia: Mapped["Colonia"] = relationship(back_populates="calles")
