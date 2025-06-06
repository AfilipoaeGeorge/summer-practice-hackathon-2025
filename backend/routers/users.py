from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from database import users_collection  # importă colecția din database.py

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    email: EmailStr
    password: str

def hash_password(password: str):
    return pwd_context.hash(password)

@router.post("/")
async def create_user(user: User):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    user_data = {"email": user.email, "hashed_password": hashed_password}
    result = users_collection.insert_one(user_data)
    return {"id": str(result.inserted_id), "email": user.email}

@router.get("/")
async def get_users():
    users = []
    for user in users_collection.find({}, {"hashed_password": 0}):
        user["id"] = str(user["_id"])
        del user["_id"]
        users.append(user)
    return users
