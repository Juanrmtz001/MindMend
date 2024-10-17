# app/auth/routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.jwt_handler import create_access_token, get_password_hash, verify_password
from app.db import db  # Import the MongoDB database object
from app.auth.models import User
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

auth_router = APIRouter()

# User signup route
@auth_router.post("/signup")
async def signup(user: User):
    # Check if the username already exists
    existing_user = await db.users.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password and save the user
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    await db.users.insert_one(user_dict)
    return {"message": "User created successfully"}

# User login route
@auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Look for user in the database
    user = await db.users.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Create JWT token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}
