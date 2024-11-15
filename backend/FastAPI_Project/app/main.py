from fastapi import FastAPI
from app.api.endpoints import item_router
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
app.include_router(item_router.router, prefix="/items", tags=["items"])
