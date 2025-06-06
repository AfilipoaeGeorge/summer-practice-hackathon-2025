from fastapi import APIRouter, HTTPException
from passlib.hash import bcrypt
from models import User
from database import db

router = APIRouter()

@router.post("/signup")
def signup(user: User):
    if db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = bcrypt.hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed
    db.users.insert_one(user_dict)
    return {"msg": "User created successfully"}

@router.post("/login")
def login(user: User):
    user_db = db.users.find_one({"email": user.email})
    if not user_db or not bcrypt.verify(user.password, user_db["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"msg": "Login successful", "user_id": str(user_db["_id"])}
