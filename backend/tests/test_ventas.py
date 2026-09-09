from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventario import Inventario


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_crear_venta_descuenta_stock(
    client: TestClient, db: Session, empleado_token: str
) -> None:
    inventario = db.scalar(select(Inventario))
    assert inventario is not None

    response = client.post(
        "/ventas",
        headers=auth_headers(empleado_token),
        json={
            "cliente_id": 1,
            "sucursal_id": inventario.sucursal_id,
            "inventario_id": inventario.id,
            "cantidad": 2,
            "metodo_pago": "Efectivo",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["total"] == 200.0
    assert len(body["detalles"]) == 1

    db.refresh(inventario)
    assert inventario.stock == 3


def test_venta_stock_insuficiente(
    client: TestClient, db: Session, empleado_token: str
) -> None:
    inventario = db.scalar(select(Inventario))
    assert inventario is not None

    response = client.post(
        "/ventas",
        headers=auth_headers(empleado_token),
        json={
            "cliente_id": 1,
            "sucursal_id": inventario.sucursal_id,
            "inventario_id": inventario.id,
            "cantidad": 999,
            "metodo_pago": "Efectivo",
        },
    )
    assert response.status_code == 400


def test_metodo_pago_invalido(
    client: TestClient, db: Session, empleado_token: str
) -> None:
    inventario = db.scalar(select(Inventario))
    assert inventario is not None

    response = client.post(
        "/ventas",
        headers=auth_headers(empleado_token),
        json={
            "cliente_id": 1,
            "sucursal_id": inventario.sucursal_id,
            "inventario_id": inventario.id,
            "cantidad": 1,
            "metodo_pago": "Bitcoin",
        },
    )
    assert response.status_code == 422
