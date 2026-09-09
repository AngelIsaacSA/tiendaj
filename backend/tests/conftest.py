from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import engine
from app.main import app
from app.models.catalogo import Clasificacion
from app.models.core import Cliente, Empleado, Sucursal
from app.models.geo import Calle, Ciudad, Colonia, Estado, Pais
from app.models.inventario import Inventario, Plataforma, Videojuego


@pytest.fixture()
def db() -> Generator[Session, None, None]:
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture()
def empleado_token(db: Session, client: TestClient) -> str:
    pais = Pais(id="MX", nombre="México")
    estado = Estado(id="MX-COA", pais=pais, nombre="Coahuila")
    ciudad = Ciudad(estado=estado, nombre="Saltillo")
    colonia = Colonia(id="COL001", ciudad=ciudad, nombre="Centro")
    calle = Calle(colonia=colonia, nombre="Av. Juárez")
    db.add_all([pais, estado, ciudad, colonia, calle])
    db.flush()

    sucursal = Sucursal(calle_id=calle.id, nombre="Centro", numero_exterior="1")
    db.add(sucursal)
    db.flush()

    empleado = Empleado(
        calle_id=calle.id,
        sucursal_id=sucursal.id,
        nombre="Test",
        apellido_paterno="User",
        apellido_materno="Qa",
        curp="TEST000101HCLXXX01",
        rfc="TEST000101ABC",
        puesto="Vendedor",
        password_hash=hash_password("secret123"),
    )
    db.add(empleado)

    clasif = Clasificacion(id="E", nombre="Everyone")
    cliente = Cliente(calle_id=calle.id, nombre="Cliente", apellido_paterno="Prueba")
    db.add_all([clasif, cliente])
    db.flush()

    videojuego = Videojuego(clasificacion_id=clasif.id, titulo="Juego Test", precio=100)
    db.add(videojuego)
    db.flush()

    plataforma = Plataforma(id="PC", videojuego_id=videojuego.id, nombre="PC")
    db.add(plataforma)
    db.flush()

    inventario = Inventario(
        plataforma_id=plataforma.id, sucursal_id=sucursal.id, nombre="A1", stock=5
    )
    db.add(inventario)
    db.commit()

    response = client.post(
        "/auth/login", json={"rfc": "TEST000101ABC", "password": "secret123"}
    )
    return response.json()["access_token"]
