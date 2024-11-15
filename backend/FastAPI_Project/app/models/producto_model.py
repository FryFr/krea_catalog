from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class Producto(BaseModel):
    id: str
    nombre: str
    precio: int
    cantidad: int

    class Config:
        json_encoders = {ObjectId: str}
