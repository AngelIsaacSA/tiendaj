from fastapi.testclient import TestClient


def test_login_invalido(client: TestClient, db) -> None:
    response = client.post(
        "/auth/login", json={"rfc": "NOEXISTE", "password": "x"}
    )
    assert response.status_code == 401


def test_login_y_me(client: TestClient, empleado_token: str) -> None:
    response = client.get(
        "/auth/me", headers={"Authorization": f"Bearer {empleado_token}"}
    )
    assert response.status_code == 200
    assert response.json()["puesto"] == "Vendedor"


def test_endpoint_protegido_sin_token(client: TestClient, db) -> None:
    response = client.get("/videojuegos")
    assert response.status_code == 401
