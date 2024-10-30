from fastapi import APIRouter, status, HTTPException, UploadFile, File, Form
from bson import ObjectId
from fastapi.responses import StreamingResponse
from db.Mongo import Base_de_Datos
import gridfs

router = APIRouter(prefix="/catalogos_pdf",
                   tags=["catalogos_pdf"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

fs = gridfs.GridFS(Base_de_Datos)

# Función para subir los PDFs
@router.post("/subir_pdf/")
async def subir_PDF(archivo: UploadFile = File(...), categoria: str = Form(...)):
    # Verificar el tipo de contenido del archivo
    if archivo.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

    # Verificar si el archivo PDF ya existe en GridFS por su nombre
    archivo_existe = Base_de_Datos.fs.files.find_one({"filename": archivo.filename})
    if archivo_existe:
        return {"mensaje": "El archivo PDF ya existe"}
    
    # Leer el contenido binario del archivo PDF
    datos_archivo = await archivo.read()

    # Guardar el archivo en GridFS
    id_archivo = fs.put(datos_archivo , filename=archivo.filename, content_type=archivo.content_type, categoria=categoria)

    return {"file_id": str(id_archivo), "filename": archivo.filename, "categoria": categoria}

    

# Función para visualizar los archivos PDFs
@router.get("/visualizar_pdf/{id_archivo}")
async def visualizar_pdf(id_archivo: str):
    try:
        # Recuperar el archivo desde GridFS
        datos_archivo = fs.get(ObjectId(id_archivo))
        if not datos_archivo:
            raise HTTPException(status_code=404, detail="Archivo no encontrado")

        # Configurar para visualizar en el navegador
        headers = {"Content-Disposition": f"inline; filename={datos_archivo.filename}"}
        
        return StreamingResponse(
            iter([datos_archivo.read()]), 
            media_type=datos_archivo.content_type,
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Función para descargar los archivos PDFs
@router.get("/descargar_pdf/{id_archivo}")
async def descargar_pdf(id_archivo: str):
    try:
        # Recuperar el archivo desde GridFS
        datos_archivo = fs.get(ObjectId(id_archivo))
        if not datos_archivo:
            raise HTTPException(status_code=404, detail="Archivo no encontrado")

        # Configurar encabezado para descarga
        headers = {"Content-Disposition": f"attachment; filename={datos_archivo.filename}"}
        
        return StreamingResponse(
            iter([datos_archivo.read()]),  # Stream del archivo binario
            media_type=datos_archivo.content_type,
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Función para eliminar los PDFs
@router.delete("/eliminar_pdf/{id_archivo}")
async def eliminar_pdf(id_archivo: str):
    try:
        datos_archivo = fs.get(ObjectId(id_archivo))
        if not datos_archivo:
            raise HTTPException(status_code=404, detail="Archivo no encontrado")

        # Eliminar el archivo desde GridFS
        fs.delete(ObjectId(id_archivo))
        return {"Mensaje": "Archivo eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))