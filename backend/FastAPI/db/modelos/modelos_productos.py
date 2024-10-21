# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=20480

### User model ###

from pydantic import BaseModel
from typing import Optional


class Producto(BaseModel):
    id: Optional[str] = None
    nombre: str
    precio: int
