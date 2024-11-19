from fastapi import FastAPI, HTTPException
from app.database import db, serialize_list, serialize_item
from app.models import ProductModel
from pymongo.errors import PyMongoError
from bson import ObjectId

app = FastAPI()

@app.get("/products", response_model=list[ProductModel])
async def get_all_products():
    try:
        # Get all products and convert cursor to a list
        products = await db["products"].find().to_list(length=None)
        
        # Convert `_id` to string on each product
        for product in products:
            product["_id"] = str(product["_id"])
        
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/products", response_model=ProductModel)
async def create_product(product: ProductModel):
    try:
        # Check if the product with the same id already exists
        existing_product = await db.products.find_one({"id": product.id})
        if existing_product:
            raise HTTPException(status_code=400, detail="A product with this ID already exists")
        
        # Convert Pydantic model into a dictionary for MongoDB
        product_dict = product.dict(exclude_unset=True)
        
        # Insert the new product into the "products" collection
        result = await db.products.insert_one(product_dict)
        
        # Get the inserted product and serialize it
        created_product = serialize_item(await db.products.find_one({"_id": result.inserted_id}))
        return created_product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{product_id}", response_model=ProductModel)
async def get_product_by_id(product_id: str):
    try:
        product = await db["products"].find_one({"id": product_id})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Convert _id to string before returning
        product["_id"] = str(product["_id"])
        return product
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail="Database error") from e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid request") from e
    
@app.put("/products/{product_id}", response_model=ProductModel)
async def update_product(product_id: str, product: ProductModel):
    try:
        # Convert Pydantic model to a dictionary for MongoDB, excluding unsent fields
        product_dict = product.dict(exclude_unset=True)
        
        # Try to update the product with the given id
        result = await db.products.update_one({"id": product_id}, {"$set": product_dict})
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Get the updated product and serialize it
        updated_product = await db.products.find_one({"id": product_id})
        return serialize_item(updated_product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/products/{product_id}", response_model=dict)
async def delete_product(product_id: str):
    try:
        # Try to delete the product with the given id
        result = await db.products.delete_one({"id": product_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return {"message": "Product successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
