from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import get_current_empleado
from app.db.session import get_db
from app.models.core import Cliente
from app.schemas.cliente import ClienteCreate, ClienteOut

router = APIRouter(
    prefix="/clientes",
    tags=["clientes"],
    dependencies=[Depends(get_current_empleado)],
)


@router.get("", response_model=list[ClienteOut])
def listar(db: Annotated[Session, Depends(get_db)]) -> list[Cliente]:
    return list(db.scalars(select(Cliente).order_by(Cliente.nombre)))


@router.post("", response_model=ClienteOut, status_code=status.HTTP_201_CREATED)
def crear(data: ClienteCreate, db: Annotated[Session, Depends(get_db)]) -> Cliente:
    cliente = Cliente(**data.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(cliente_id: int, db: Annotated[Session, Depends(get_db)]) -> None:
    cliente = db.get(Cliente, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")
    db.delete(cliente)
    db.commit()
