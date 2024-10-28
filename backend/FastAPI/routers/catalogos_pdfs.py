
from fastapi import APIRouter, status, HTTPException, UploadFile, File
from bson import ObjectId, Binary
from fastapi.responses import StreamingResponse
from db.Mongo import Base_de_Datos

router = APIRouter(prefix="/catalogos_pdf",
                   tags=["catalogos_pdf"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


# Función para subir los archvios PDFs
@router.post("/subir_pdf/")
async def subir_PDF(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

    # Verificar si el archivo PDF ya existe
    archivo_existe = Base_de_Datos.PDFs.find_one({"filename": file.filename})
    if archivo_existe:
        return {"mensaje": "El archivo PDF ya existe"}
    
    # Leer el contenido binario del archivo PDF
    file_data = await file.read()

    # Guardar el archivo en MongoDB como datos binarios
    file_id = Base_de_Datos.PDFs.insert_one({
        "filename": file.filename,
        "file_data": Binary(file_data),
        "content_type": file.content_type
    }).inserted_id

    return {"file_id": str(file_id), "filename": file.filename}
    

# Función para visualizar los archivos PDFs
@router.get("/visualizar_pdf/{file_id}")
async def visualizar_pdf(file_id: str):
    try:
        # Recuperar el documento que contiene el PDF
        file_doc = Base_de_Datos.PDFs.find_one({"_id": ObjectId(file_id)})
        if not file_doc:
            raise HTTPException(status_code=404, detail="Archivo no encontrado")

        # Configurar para visualizar en el navegador
        headers = {"Content-Disposition": f"inline; filename={file_doc['filename']}"}
        
        return StreamingResponse(
            iter([file_doc["file_data"]]), 
            media_type=file_doc["content_type"],
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Función para descargar los archivos PDFs
@router.get("/descargar_pdf/{file_id}")
async def descargar_pdf(file_id: str):
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

@router.delete("/eliminar_pdf/{file_id}")
async def eliminar_pdf(file_id: str):
    # Intentar eliminar el documento que contiene el PDF
    result = Base_de_Datos.PDFs.delete_one({"_id": ObjectId(file_id)})

    # Verificar si se eliminó algún documento
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    return {"Mensaje": "Archivo eliminado correctamente"}