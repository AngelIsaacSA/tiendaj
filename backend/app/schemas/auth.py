from pydantic import BaseModel


class LoginRequest(BaseModel):
    rfc: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class EmpleadoOut(BaseModel):
    id: int
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    puesto: str

    model_config = {"from_attributes": True}
