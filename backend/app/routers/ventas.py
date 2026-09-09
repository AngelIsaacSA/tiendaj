from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.auth import get_current_empleado
from app.db.session import get_db
from app.models.core import Empleado
from app.models.inventario import Inventario
from app.models.venta import DetalleVenta, Venta
from app.schemas.venta import VentaCreate, VentaOut

router = APIRouter(
    prefix="/ventas",
    tags=["ventas"],
    dependencies=[Depends(get_current_empleado)],
)


@router.get("", response_model=list[VentaOut])
def listar(db: Annotated[Session, Depends(get_db)]) -> list[Venta]:
    stmt = (
        select(Venta)
        .options(selectinload(Venta.detalles))
        .order_by(Venta.fecha_venta.desc())
    )
    return list(db.scalars(stmt))


@router.post("", response_model=VentaOut, status_code=status.HTTP_201_CREATED)
def crear(
    data: VentaCreate,
    db: Annotated[Session, Depends(get_db)],
    empleado: Annotated[Empleado, Depends(get_current_empleado)],
) -> Venta:
    try:
        data.validar_metodo_pago()
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)) from exc

    inventario = db.get(Inventario, data.inventario_id)
    if inventario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventario no encontrado")
    if inventario.stock < data.cantidad:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stock insuficiente. Disponible: {inventario.stock}",
        )

    videojuego = inventario.plataforma.videojuego
    subtotal = float(videojuego.precio) * data.cantidad

    venta = Venta(
        cliente_id=data.cliente_id,
        sucursal_id=data.sucursal_id,
        empleado_id=empleado.id,
        total=subtotal,
        metodo_pago=data.metodo_pago,
    )
    venta.detalles.append(
        DetalleVenta(
            videojuego_id=videojuego.id,
            cantidad=data.cantidad,
            precio_unitario=videojuego.precio,
            subtotal=subtotal,
        )
    )
    inventario.stock -= data.cantidad

    db.add(venta)
    db.commit()
    db.refresh(venta)
    return venta
