from pydantic import BaseModel
from typing import Optional

class ItemSchema(BaseModel):
    id: str
    nombre: str
    precio: int
    cantidad: int
