from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import get_current_empleado
from app.db.session import get_db
from app.models.inventario import Videojuego
from app.schemas.videojuego import VideojuegoCreate, VideojuegoOut

router = APIRouter(
    prefix="/videojuegos",
    tags=["videojuegos"],
    dependencies=[Depends(get_current_empleado)],
)


@router.get("", response_model=list[VideojuegoOut])
def listar(db: Annotated[Session, Depends(get_db)]) -> list[Videojuego]:
    return list(db.scalars(select(Videojuego).order_by(Videojuego.titulo)))


@router.post("", response_model=VideojuegoOut, status_code=status.HTTP_201_CREATED)
def crear(data: VideojuegoCreate, db: Annotated[Session, Depends(get_db)]) -> Videojuego:
    videojuego = Videojuego(**data.model_dump())
    db.add(videojuego)
    db.commit()
    db.refresh(videojuego)
    return videojuego


@router.delete("/{videojuego_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(videojuego_id: int, db: Annotated[Session, Depends(get_db)]) -> None:
    videojuego = db.get(Videojuego, videojuego_id)
    if videojuego is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")
    db.delete(videojuego)
    db.commit()
