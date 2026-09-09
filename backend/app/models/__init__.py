from app.models.catalogo import Clasificacion, Genero
from app.models.contacto import Correo, Telefono
from app.models.core import Cliente, Empleado, Proveedor, Sucursal
from app.models.geo import Calle, Ciudad, Colonia, Estado, Pais
from app.models.inventario import Inventario, Plataforma, Videojuego
from app.models.venta import DetalleVenta, Venta

__all__ = [
    "Calle",
    "Ciudad",
    "Clasificacion",
    "Cliente",
    "Colonia",
    "Correo",
    "DetalleVenta",
    "Empleado",
    "Estado",
    "Genero",
    "Inventario",
    "Pais",
    "Plataforma",
    "Proveedor",
    "Sucursal",
    "Telefono",
    "Venta",
    "Videojuego",
]
