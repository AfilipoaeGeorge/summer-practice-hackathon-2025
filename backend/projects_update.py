from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel
from database import projects_collection, users_collection
from bson import ObjectId

router = APIRouter()

class ProjectUpdate(BaseModel):
    title: str | None = None
    body: str | None = None

def serialize_project(project: dict) -> dict:
    project["id"] = str(project["_id"])
    del project["_id"]
    return project

@router.put("/{project_id}")
async def update_project(
    project_id: str,
    update_data: ProjectUpdate,
    user_email: str 
):
    if not users_collection.find_one({"email": user_email}):
        raise HTTPException(status_code=400, detail="User email does not exist")
    
    existing_project = projects_collection.find_one({"_id": ObjectId(project_id), "user_email": user_email})
    if not existing_project:
        raise HTTPException(status_code=404, detail="Project not found or you don't have permission to update it")
    
    update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
    if not update_dict:
        raise HTTPException(status_code=400, detail="No data to update")
    
    projects_collection.update_one({"_id": ObjectId(project_id)}, {"$set": update_dict})
    updated_project = projects_collection.find_one({"_id": ObjectId(project_id)})
    return serialize_project(updated_project)
