from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import create_access_token, get_current_empleado
from app.core.security import verify_password
from app.db.session import get_db
from app.models.core import Empleado
from app.schemas.auth import EmpleadoOut, LoginRequest, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Annotated[Session, Depends(get_db)]) -> Token:
    empleado = db.scalar(select(Empleado).where(Empleado.rfc == data.rfc))
    if (
        empleado is None
        or empleado.password_hash is None
        or not verify_password(data.password, empleado.password_hash)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="RFC o contraseña incorrectos",
        )
    return Token(access_token=create_access_token(str(empleado.id)))


@router.get("/me", response_model=EmpleadoOut)
def me(empleado: Annotated[Empleado, Depends(get_current_empleado)]) -> Empleado:
    return empleado
