from fastapi import FastAPI
from routers import catalogos_pdfs, productos
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Router para los productos
app.include_router(productos.router)

# Router para los catalogos
app.include_router(catalogos_pdfs.router)

# Recuros estáticos
app.mount("/recursos_estaticos", StaticFiles(directory="recursos_estaticos"), name="recursos_estaticos")
