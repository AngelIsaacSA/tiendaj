from datetime import date

from pydantic import BaseModel, Field


class VideojuegoBase(BaseModel):
    titulo: str
    precio: float = Field(gt=0)
    clasificacion_id: str
    fecha_lanzamiento: date | None = None


class VideojuegoCreate(VideojuegoBase):
    pass


class VideojuegoOut(VideojuegoBase):
    id: int

    model_config = {"from_attributes": True}
