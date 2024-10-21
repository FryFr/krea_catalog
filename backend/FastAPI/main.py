# Activar entorno virutal con las dependencias instaladas: .venv\Scripts\Activate.ps1

# Instala FastAPI: pip install "fastapi[all]"

from fastapi import FastAPI
from routers import productos_Base_de_Datos
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=20480
app.include_router(productos_Base_de_Datos.router)

# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=13618
app.mount("/recursos_estaticos", StaticFiles(directory="recursos_estaticos"), name="recursos_estaticos")


# Url local: http://127.0.0.1:8000


@app.get("/")
async def root():
    return "Hola FastAPI!"

# Url local: http://127.0.0.1:8000/url


@app.get("/url")
async def url():
    return {"url": "https://mouredev.com/python"}

# Inicia el server: uvicorn main:app --reload
# Detener el server: CTRL+C

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc
