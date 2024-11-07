Para ejecutar el backend es necesario primero activar el entorno virutal:

    ruta: Proyecto Krea\krea_catalog\backend
    comando: .venv\Scripts\Activate.ps1

Tambien es necesario instalar las siguientes dependencias en dicho entorno virutal:

    pip install "fastapi[all]"
    pip install pymongo
    pip install pydantic
    pip install uvicorn

Ahora es necesario iniciar el servidor:

    ruta: Proyecto Krea\krea_catalog\backend\FastAPI
    comando: uvicorn main:app --reload

La URL local del servidor es: http://127.0.0.1:8000

Toda la documentación de las peticiones HTTP puede hallarse en las siguientes rutas:

    Swagger: http://127.0.0.1:8000/docs
    Redocly: http://127.0.0.1:8000/redoc