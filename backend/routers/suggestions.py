from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import suggestions_collection
from database import users_collection

router = APIRouter()

class Suggestion(BaseModel):
    user_email: str
    content: Optional [str] = None

def serialize_suggestion(suggestion: dict) -> dict:
    suggestion["id"] = str(suggestion["_id"])
    del suggestion["_id"]
    return suggestion

@router.post("/")
async def create_suggestion(suggestion: Suggestion):
    user_exists = users_collection.find_one({"email": suggestion.user_email})
    if not user_exists:
        raise HTTPException(status_code=400, detail="User email does not exist")
    
    suggestion_dict = suggestion.dict()
    result = suggestions_collection.insert_one(suggestion_dict)
    created_suggestion = suggestions_collection.find_one({"_id": result.inserted_id})
    return serialize_suggestion(created_suggestion)

@router.get("/")
async def get_suggestions():
    suggestions = []
    for s in suggestions_collection.find():
        s["id"] = str(s["_id"])
        del s["_id"]
        suggestions.append(s)
    return suggestions