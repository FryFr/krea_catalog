from fastapi import APIRouter, HTTPException, Depends
from app.models.producto_model import Producto
from app.schemas.item_schema import ItemSchema
from app.db.mongodb import db
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=Producto)
async def create_item(item: ItemSchema):
    item_dict = item.dict()
    result = await db.database["items"].insert_one(item_dict)
    item_dict["_id"] = result.inserted_id
    return item_dict

@router.get("/{item_id}", response_model=Producto)
async def read_item(item_id: str):
    item = await db.database["items"].find_one({"_id": ObjectId(item_id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=Producto)
async def update_item(item_id: str, item: ItemSchema):
    result = await db.database["items"].update_one({"_id": ObjectId(item_id)}, {"$set": item.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return await read_item(item_id)

@router.delete("/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    result = await db.database["items"].delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}
