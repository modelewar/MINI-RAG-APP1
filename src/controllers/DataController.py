import os
from .BaseController import BaseController
from fastapi import UploadFile 
from models import ResponseSignal
from .ProjectController import ProjectController
import re

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576  # 1 MB in bytes
    
    #### Validate uploaded file properties:[ type, size ]
    def validate_data(self,file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False ,ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size is not None and file.size > self.app_settings.FILE_MAX_SIZE*self.size_scale:
            return False ,ResponseSignal.FILE_SIZE_EXCEEDS_LIMIT.value 
        
        return True ,ResponseSignal.FILE_VALIDATE_SUCCESS.value 
    
    
    
    def generate_unique_filepath(self, orig_filename: str,project_id:str): 
        
        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)
        
        cleaned_filename = self.get_clean_file_name(
            orig_file_name = orig_filename
        )
        
        new_file_path = os.path.join(
            project_path,
            random_key + "_" + cleaned_filename  
        )
        
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                random_key + "_" + cleaned_filename  
            )
        return new_file_path,random_key + "_" + cleaned_filename   
    
    def get_clean_file_name(self, orig_file_name: str):

        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name
    