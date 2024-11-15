from fastapi import APIRouter, HTTPException, Depends
from app.models.products_model import ProductModel
from app.schemas.products_schema import ItemSchema
from app.db.mongodb import db
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=ProductModel)
async def create_item(item: ItemSchema):
    item_dict = item.dict()
    result = await db.database["products"].insert_one(item_dict)
    item_dict["_id"] = result.inserted_id
    return item_dict

@router.get("/{product_id}", response_model=ProductModel)
async def read_item(product_id: str):
    item = await db.database["products"].find_one({"_id": ObjectId(product_id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{product_id}", response_model=ProductModel)
async def update_item(product_id: str, item: ItemSchema):
    result = await db.database["products"].update_one({"_id": ObjectId(product_id)}, {"$set": item.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return await read_item(product_id)

@router.delete("/{product_id}", response_model=dict)
async def delete_item(product_id: str):
    result = await db.database["products"].delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}
