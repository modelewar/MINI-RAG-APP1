from fastapi import  APIRouter, Depends,UploadFile, status
from helpers.config import get_settings , Settings
from controllers import DataController , ProjectController,ProcessController
from fastapi.responses import JSONResponse 
import os
import aiofiles
from models import ResponseSignal 
import logging
from .schemes.data import ProcessRequest

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str ,file:UploadFile,
                     app_settings:Settings = Depends(get_settings)):
    #validate the file properties
    data_controller = DataController()
    
    is_valid,result_signal = data_controller.validate_data(file)    
    
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
             
            content={"is_valid":is_valid,
                     "message":result_signal
                    }
        )
        
    project_dir_path = ProjectController().get_project_path(project_id=project_id) 
    
    is_valid,result_signal = data_controller.validate_data(file)    
        
    file_path ,file_id =  data_controller.generate_unique_filepath(
        orig_filename = file.filename,
        project_id=project_id
    )

    try:
        async with aiofiles.open(file_path,'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        
        logger.error(f"Error uploading file: {e}")
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "signal":ResponseSignal.DATA_UPLOADED_FAILURE.value,
                "error":str(e)
            }
        )        
    
    return JSONResponse(
        content={
            "signal":ResponseSignal.DATA_UPLOAD_SUCCESS.value,
            "file_id":file_id
        }
    )
    
@data_router.post("/process/{project_id}")
async def process_enpoint(project_id:str, process_request:ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    
    
    process_controller = ProcessController(project_id=project_id)
    
    file_content = process_controller.get_file_content(file_id=file_id)
    
    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        chunk_size=chunk_size,
        chunk_overlap=overlap_size
    )

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "signal":ResponseSignal.DATA_PROCESSING_FAILURE.value,
                "error":"Failed to process file content"
            }
        )
    return file_chunks