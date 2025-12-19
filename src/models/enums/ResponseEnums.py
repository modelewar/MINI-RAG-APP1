from enum import Enum

class ResponseSignal(Enum):
    FILE_VALIDATE_SUCCESS = "file is successfully validated"
    FILE_TYPE_NOT_SUPPORTED = "file type not supported"
    FILE_SIZE_EXCEEDS_LIMIT = "file size exceeds the maximum limit"
    DATA_UPLOAD_SUCCESS = "data uploaded successfully"
    DATA_UPLOADED_FAILURE = "data upload failed"
    PROCESSING_SUCCESS = "file processed successfully"
    DATA_PROCESSING_FAILURE = "data processing failed"