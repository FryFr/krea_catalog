---------------- New documentation ----------------

Para comenzar con la ejecucion del proyecto de FastAPI se debe seguir los siguientes pasos:

Ingresa a la carpeta backend
    Ruta: cd Krea\krea_catalog\backend

Crear el entorno virutal
    comando: python -m venv venv

Inicializar el entorno virutal
    comando: .\venv\Scripts\Activate.ps1

Actualizacion del pip
    comando: python -m pip install --upgrade pip

Instalacion de los requerimientos
    comando: pip install -r requirements.txt

Ahora es necesario iniciar el servidor:

    ruta: Proyecto Krea\krea_catalog\backend\FastAPI
    comando: uvicorn main:app --reload
    command 2: uvicorn app.main:app --reload

La URL local del servidor es: http://127.0.0.1:8000

Toda la documentación de las peticiones HTTP puede hallarse en las siguientes rutas:

    Swagger: http://127.0.0.1:8000/docs
    Redocly: http://127.0.0.1:8000/redoc

---------------- Previous documentation ----------------

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
    Comand: uvicorn app.main:app --reload 

La URL local del servidor es: http://127.0.0.1:8000

Toda la documentación de las peticiones HTTP puede hallarse en las siguientes rutas:

    Swagger: http://127.0.0.1:8000/docs
    Redocly: http://127.0.0.1:8000/redoc