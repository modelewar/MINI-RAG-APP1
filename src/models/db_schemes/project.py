from pydantic import BaseModel, Field,validator
from typing import Optional
from bson.objectid import ObjectId


class Project(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")  
    project_id:str = Field(..., min_length=1)
    
    
     # The way to design a custom validation on the schemes
    @validator('project_id') 
    def validate_project_id(cls, value):
          if not value.isalnum():  
              raise ValueError('project_id must be Alphanumeric')
         
          return value 
    
    
    class Config:
        arbitrary_types_allowed = True
              