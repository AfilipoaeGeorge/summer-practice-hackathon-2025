from fastapi import APIRouter, HTTPException
from models import Project
from pydantic import BaseModel
from database import db
from database import projects_collection
from database import users_collection

router = APIRouter()

class Project(BaseModel):
    user_email: str
    title: str
    body: str


def serialize_project(project: dict) -> dict:
    project["id"] = str(project["_id"])
    del project["_id"]
    return project


@router.post("/")
async def create_project(project: Project):
    user_exists = users_collection.find_one({"email": project.user_email})
    if not user_exists:
        raise HTTPException(status_code=400, detail="User email does not exist")
    
    project_dict = project.dict()
    result = projects_collection.insert_one(project_dict)
    created_project = projects_collection.find_one({"_id": result.inserted_id})
    return serialize_project(created_project)


@router.get("/")
async def get_projects():
    projects = []
    for p in projects_collection.find():
        p["id"] = str(p["_id"])
        del p["_id"]
        projects.append(p)
    return projects