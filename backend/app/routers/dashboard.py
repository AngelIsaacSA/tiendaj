from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.core.auth import get_current_empleado
from app.db.session import get_db
from app.models.core import Cliente
from app.models.inventario import Videojuego
from app.models.venta import Venta
from app.schemas.dashboard import DashboardStats

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    dependencies=[Depends(get_current_empleado)],
)


@router.get("", response_model=DashboardStats)
def stats(db: Annotated[Session, Depends(get_db)]) -> DashboardStats:
    total_videojuegos = db.scalar(select(func.count()).select_from(Videojuego)) or 0
    total_clientes = db.scalar(select(func.count()).select_from(Cliente)) or 0
    total_ventas = db.scalar(select(func.count()).select_from(Venta)) or 0
    ingresos = db.scalar(select(func.coalesce(func.sum(Venta.total), 0))) or 0

    ultimas_ventas = list(
        db.scalars(
            select(Venta)
            .options(selectinload(Venta.detalles))
            .order_by(Venta.fecha_venta.desc())
            .limit(5)
        )
    )

    return DashboardStats(
        total_videojuegos=total_videojuegos,
        total_clientes=total_clientes,
        total_ventas=total_ventas,
        ingresos=float(ingresos),
        ultimas_ventas=ultimas_ventas,
    )
