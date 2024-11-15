from fastapi import FastAPI
from app.api.endpoints import products_router
from app.db.mongodb import connect_db, close_db

app = FastAPI()

# Conectar y desconectar MongoDB
@app.on_event("startup")
async def startup_db_client():
    await connect_db()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_db()

# Registro de rutas
app.include_router(products_router.router, prefix="/product", tags=["product"])
