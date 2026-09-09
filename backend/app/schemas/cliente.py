from pydantic import BaseModel


class ClienteBase(BaseModel):
    nombre: str | None = None
    apellido_paterno: str | None = None
    apellido_materno: str | None = None
    calle_id: int


class ClienteCreate(ClienteBase):
    pass


class ClienteOut(ClienteBase):
    id: int

    model_config = {"from_attributes": True}
