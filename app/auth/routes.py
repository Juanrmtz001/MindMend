# app/auth/routes.py
from fastapi import APIRouter, Depends, HTTPException
from app.auth.models import User
from app.db import db  # Import the db object
from app.auth.jwt_handler import create_access_token
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter()

# Signup route
@auth_router.post("/signup")
async def signup(user: User):
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict['hashed_password'] = hashed_password
    del user_dict['password']
    await db.users.insert_one(user_dict)  # Using the db object from app.db
    return {"message": "User created successfully"}

# Login route
@auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db.users.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user['username']})
    return {"access_token": access_token, "token_type": "bearer"}
