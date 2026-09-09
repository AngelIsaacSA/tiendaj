"""Datos de ejemplo para desarrollo local. Ejecutar con: python -m app.seed"""

from datetime import date

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import (
    Calle,
    Ciudad,
    Clasificacion,
    Cliente,
    Colonia,
    Empleado,
    Estado,
    Genero,
    Inventario,
    Pais,
    Plataforma,
    Proveedor,
    Sucursal,
    Videojuego,
)


def seed() -> None:
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        if db.query(Pais).first():
            print("Ya hay datos, no se vuelve a sembrar.")
            return

        mexico = Pais(id="MX", nombre="México")
        coahuila = Estado(id="MX-COA", pais=mexico, nombre="Coahuila")
        saltillo = Ciudad(estado=coahuila, nombre="Saltillo")
        centro = Colonia(id="COL001", ciudad=saltillo, nombre="Centro")
        juarez = Calle(colonia=centro, nombre="Av. Juárez")
        db.add_all([mexico, coahuila, saltillo, centro, juarez])
        db.flush()

        sucursal = Sucursal(
            calle_id=juarez.id, nombre="Sucursal Centro", numero_exterior="100"
        )
        db.add(sucursal)
        db.flush()

        empleado = Empleado(
            calle_id=juarez.id,
            sucursal_id=sucursal.id,
            nombre="Angel",
            apellido_paterno="Isaacs",
            apellido_materno="Admin",
            curp="ISAA000101HCLXXX01",
            rfc="ISAA000101ABC",
            puesto="Administrador",
            password_hash=hash_password("admin123"),
        )
        db.add(empleado)

        clasif_e = Clasificacion(id="E", nombre="Everyone")
        clasif_m = Clasificacion(id="M", nombre="Mature")
        db.add_all([clasif_e, clasif_m])

        db.add(Genero(id="ACC", nombre="Acción"))

        proveedor = Proveedor(nombre="Distribuidora Games MX", rfc="DGM010101XYZ")
        db.add(proveedor)

        cliente = Cliente(
            calle_id=juarez.id,
            nombre="Juan",
            apellido_paterno="Pérez",
            apellido_materno="López",
        )
        db.add(cliente)
        db.flush()

        juego = Videojuego(
            clasificacion_id=clasif_m.id,
            titulo="The Legend of Zelda: Tears of the Kingdom",
            precio=1299.00,
            fecha_lanzamiento=date(2023, 5, 12),
        )
        db.add(juego)
        db.flush()

        plataforma = Plataforma(id="NSW", videojuego_id=juego.id, nombre="Nintendo Switch")
        db.add(plataforma)
        db.flush()

        inventario = Inventario(
            plataforma_id=plataforma.id,
            sucursal_id=sucursal.id,
            nombre="Estante A1",
            stock=15,
        )
        db.add(inventario)

        db.commit()
        print("Datos de ejemplo insertados.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
