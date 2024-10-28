from fastapi import APIRouter, HTTPException, status, FastAPI
from bson import ObjectId, Binary
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient

app = FastAPI()


### Esquema para los productos ###

def esquema_producto(producto) -> dict:
    return {"id": str(producto["_id"]), # Convierte el '_id' del producto en una cadena.
            "nombre": producto["nombre"], # Extrae el 'nombre' del producto.
            "precio": producto["precio"],
            "cantidad": producto["cantidad"]}  # Extrae el 'precio' del producto.


def esquema_producto2(producto) -> dict:
    return {"id": str(producto["_id"]), # Convierte el '_id' del producto en una cadena.
            "nombre": producto["nombre"], # Extrae el 'nombre' del producto.
            "precio": producto["precio"],
            "cantidad": producto["cantidad"],
            "otra_cosa": producto["otra_cosa"]}  # Extrae el 'precio' del producto.


def esquema_productos(productos) -> list:
    return [esquema_producto(producto) for producto in productos] # Itera sobre cada producto en la lista "productos" y aplica la función "esquema_producto()" a cada uno.
 
### Modelo del producto ###
class Producto(BaseModel):
    id: Optional[str] = None
    nombre: str
    precio: int
    cantidad: int


class Producto_2(BaseModel):
    id: Optional[str] = None
    nombre: str
    precio: int
    cantidad: int
    otra_cosa: str


# Base de datos local MongoDB
Base_de_Datos = MongoClient().Productos


# Función para buscar los productos

def buscar_productos(field: str, key):
    try:
        user = Base_de_Datos.Productos.find_one({field: key})
        return Producto(**esquema_producto(user))
    except:
        return {"error": "No se ha encontrado el usuario"}


@app.get("/", response_model=list[Producto])
async def traer_productos():
    return esquema_productos(Base_de_Datos.Productos.find())


@app.get("/{id}")  # Path
async def traer_productos_por_id(id: str):
    return buscar_productos("_id", ObjectId(id))


@app.get("/")  # Query
async def traer_productos_por_id(id: str):
    return buscar_productos("_id", ObjectId(id))


@app.post("/", response_model=Producto, status_code=status.HTTP_201_CREATED)
async def crear_productos(producto: Producto):
    if type(buscar_productos("nombre", producto.nombre)) == Producto:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="El producto ya existe")

    producto_dict = dict(producto)
    del producto_dict["id"]

    id = Base_de_Datos.Productos.insert_one(producto_dict).inserted_id

    new_user = esquema_producto(Base_de_Datos.Productos.find_one({"_id": id}))

    return Producto(**new_user)

@app.post("/prueba")
async def prueba(producto: Producto_2):
    producto_dict = dict(producto)
    del producto_dict["id"]

    id = Base_de_Datos.prueba.insert_one(producto_dict).inserted_id
    nueva_prueba = esquema_producto2(Base_de_Datos.prueba.find_one({"_id": id}))
    return Producto_2(**nueva_prueba)

@app.put("/", response_model=Producto)
async def editar_producto(producto: Producto):

    producto_dict = dict(producto)
    del producto_dict["id"]

    try:
        Base_de_Datos.Productos.find_one_and_replace(
            {"_id": ObjectId(producto.id)}, producto_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}

    return buscar_productos("_id", ObjectId(producto.id))


@app.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(id: str):

    found = Base_de_Datos.Productos.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "No se ha eliminado el usuario"}


from fastapi import UploadFile, File
from bson import ObjectId
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
from fastapi.responses import StreamingResponse
    

@app.post("/catalogo_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

    # Leer el contenido binario del archivo PDF
    file_data = await file.read()

    # Guardar el archivo en MongoDB como datos binarios
    file_id = Base_de_Datos.PDFs.insert_one({
        "filename": file.filename,
        "file_data": Binary(file_data),
        "content_type": file.content_type
    }).inserted_id

    return {"file_id": str(file_id), "filename": file.filename}
    

@app.get("/catalogo_pdf/{file_id}")
async def view_pdf(file_id: str):
    try:
        # Recuperar el documento que contiene el PDF
        file_doc = Base_de_Datos.PDFs.find_one({"_id": ObjectId(file_id)})
        if not file_doc:
            raise HTTPException(status_code=404, detail="Archivo no encontrado")

        # Configurar para visualizar en el navegador
        headers = {"Content-Disposition": f"inline; filename={file_doc['filename']}"}
        
        return StreamingResponse(
            iter([file_doc["file_data"]]),  # Stream directo del campo binario
            media_type=file_doc["content_type"],
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/descargar_catalogo_pdf/{file_id}")
async def download_pdf(file_id: str):
    try:
        # Recuperar el documento que contiene el PDF
        file_doc = Base_de_Datos.PDFs.find_one({"_id": ObjectId(file_id)})
        if not file_doc:
            raise HTTPException(status_code=404, detail="Archivo no encontrado")

        # Configurar encabezado para descarga
        headers = {"Content-Disposition": f"attachment; filename={file_doc['filename']}"}
        
        return StreamingResponse(
            iter([file_doc["file_data"]]),  # Stream del archivo binario
            media_type=file_doc["content_type"],
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/catalogo_pdf/{file_id}", status_code=204)
async def delete_pdf(file_id: str):
    # Intentar eliminar el documento que contiene el PDF
    result = Base_de_Datos.PDFs.delete_one({"_id": ObjectId(file_id)})

    # Verificar si se eliminó algún documento
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    return {"message": "Archivo eliminado correctamente"}