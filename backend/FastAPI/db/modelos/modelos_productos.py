### Modelo producto ###

from pydantic import BaseModel
from typing import Optional

class Producto(BaseModel):
    id: str
    nombre: str
    precio: int
    cantidad: int
