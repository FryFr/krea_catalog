### Modelo producto ###

from pydantic import BaseModel
from typing import Optional


class Producto(BaseModel):
    id: Optional[str] = None
    nombre: str
    precio: int
    cantidad: int
