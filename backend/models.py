from pydantic import BaseModel, EmailStr
from typing import Optional, List

class User(BaseModel):
    username: str
    email: EmailStr
    password: str

class Project(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = ""
    code: str

class Comment(BaseModel):
    project_id: str
    user_id: str
    content: str

class Task(BaseModel):
    project_id: str
    user_id: str
    description: str
    completed: bool = False

class Suggestion(BaseModel):
    project_id: str
    content: str
