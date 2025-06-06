from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from fastapi import Query
from database import comments_collection, users_collection, projects_collection

router = APIRouter()

class Comment(BaseModel):
    user_email: str
    project_id: str
    content: str

def serialize_comment(comment: dict) -> dict:
    comment["id"] = str(comment["_id"])
    del comment["_id"]
    return comment

@router.post("/")
async def create_comment(comment: Comment):
    user = users_collection.find_one({"email": comment.user_email})
    if not user:
        raise HTTPException(status_code=400, detail="User email does not exist")
    
    try:
        project_obj_id = ObjectId(comment.project_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid project_id format")

    project = projects_collection.find_one({"_id": project_obj_id})
    if not project:
        raise HTTPException(status_code=400, detail="Project does not exist")

    comment_dict = comment.dict()
    result = comments_collection.insert_one(comment_dict)
    created_comment = comments_collection.find_one({"_id": result.inserted_id})
    return serialize_comment(created_comment)

@router.get("/")
async def get_comments(project_id: str = Query(..., description="ID-ul proiectului pentru care se cer comentariile")):
    try:
        project_obj_id = ObjectId(project_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid project_id format")

    project = projects_collection.find_one({"_id": project_obj_id})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    comments = []
    for c in comments_collection.find({"project_id": project_id}):
        c["id"] = str(c["_id"])
        del c["_id"]
        comments.append(c)

    return comments