from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# In-memory database (dictionary)
users_db: Dict[int, dict] = {}

# Pydantic model for request body validation
class User(BaseModel):
    name: str
    email: str
    age: int

# 📌 CREATE (POST) - Add a new user
@app.post("/users/{user_id}")
def create_user(user_id: int, user: User):
    if user_id in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user_id] = user.dict()
    return {"message": "User created successfully", "user": users_db[user_id]}

# 📌 READ (GET) - Get user by ID
@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

# 📌 UPDATE (PUT) - Modify user data
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = user.dict()
    return {"message": "User updated successfully", "user": users_db[user_id]}

# 📌 DELETE (DELETE) - Remove user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted successfully"}
