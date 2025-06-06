from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from database import tasks_collection

router = APIRouter()

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

def serialize_task(task: dict) -> dict:
    task["id"] = str(task["_id"])
    del task["_id"]
    return task

@router.post("/")
async def create_task(task: Task):
    task_dict = task.dict()
    result = tasks_collection.insert_one(task_dict)
    created_task = tasks_collection.find_one({"_id": result.inserted_id})
    return serialize_task(created_task)

@router.get("/")
async def get_tasks():
    tasks = []
    for task in tasks_collection.find():
        tasks.append(serialize_task(task))
    return tasks
