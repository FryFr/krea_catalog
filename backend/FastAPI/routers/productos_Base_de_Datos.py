# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=20480

### Users DB API ###

from fastapi import APIRouter, HTTPException, status
from db.modelos.modelos_productos import Producto
from db.esquemas.esquemas_productos import esquema_producto, esquema_productos
from db.Mongo import Base_de_Datos
from bson import ObjectId

router = APIRouter(prefix="/productos_catalogo",
                   tags=["productos_catalogo"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

# Función para buscar los productos

def buscar_productos(field: str, key):
    try:
        user = Base_de_Datos.Productos.find_one({field: key})
        return Producto(**esquema_producto(user))
    except:
        return {"error": "No se ha encontrado el usuario"}


@router.get("/", response_model=list[Producto])
async def traer_productos():
    return esquema_productos(Base_de_Datos.Productos.find())


@router.get("/{id}")  # Path
async def traer_productos_por_id(id: str):
    return buscar_productos("_id", ObjectId(id))


@router.get("/")  # Query
async def traer_productos_por_id(id: str):
    return buscar_productos("_id", ObjectId(id))


@router.post("/", response_model=Producto, status_code=status.HTTP_201_CREATED)
async def crear_productos(producto: Producto):
    if type(buscar_productos("nombre", producto.nombre)) == Producto:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="El usuario ya existe")

    producto_dict = dict(producto)
    del producto_dict["id"]

    id = Base_de_Datos.Productos.insert_one(producto_dict).inserted_id

    new_user = esquema_producto(Base_de_Datos.Productos.find_one({"_id": id}))

    return Producto(**new_user)


@router.put("/", response_model=Producto)
async def editar_producto(producto: Producto):

    producto_dict = dict(producto)
    del producto_dict["id"]

    try:
        Base_de_Datos.Productos.find_one_and_replace(
            {"_id": ObjectId(producto.id)}, producto_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}

    return buscar_productos("_id", ObjectId(producto.id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(id: str):

    found = Base_de_Datos.Productos.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "No se ha eliminado el usuario"}

