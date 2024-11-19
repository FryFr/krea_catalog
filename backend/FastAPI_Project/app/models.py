from pydantic import BaseModel

# Serializer for products
class ProductModel(BaseModel):
    id: str
    name: str
    price: float
    quantity: int

    class Config:
        from_attributes = True
