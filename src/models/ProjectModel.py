from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum



class ProjectModel(BaseDataModel):
    
    def __init__(self , db_client:object):
        super().__init__(db_client= db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
        
        
    async def create_project(self ,project:Project):
        
        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True))
        project._id = result.inserted_id
        return project
    
    
    async def get_project_or_create_one(self,project_id :str):
        record = await self.collection.find_one({ 
            "project_id": project_id     
        })
        
        if record is None :
            # Create a new project
            project = Project(project_id=project_id)
            
            project = await self.create_project(project=project)
            return project
        
        return Project(**record)
    
    async def get_all_projects(self, page:int =1 ,page_Size:int =10):
        
        # count the number of all documnents in the collection
        total_documents = await self.collection.count_document({})
        
        # calculate total number of pages 
        total_pages = total_documents // page_Size
        if total_documents % page_Size != 0:
            total_pages += 1
            
        cursor = self.collection.find().skip((page - 1) * page_Size).limit(page_Size)
        projects = []
        async for document in cursor:
            projects.append(
                Project(**document)
            )    
            
        return projects , total_pages