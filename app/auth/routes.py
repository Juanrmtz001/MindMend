from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.jwt_handler import create_access_token, get_password_hash, verify_password
from app.db import db  # Import the MongoDB database object
from app.auth.models import User
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

auth_router = APIRouter()

# User signup route
@auth_router.post("/signup")
async def signup(user: User):
    # Check if the username already exists
    existing_user = db.users.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if the email already exists
    existing_email = db.users.find_one({"email": user.email})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password and store the user in the database
    hashed_password = get_password_hash(user.password)
    
    # Prepare user data to store in the database
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]  # Remove plaintext password

    # Ensure the birthday is in the correct format
    if isinstance(user_dict.get("birthday"), str):
        # Parse the string date to a datetime object
        user_dict["birthday"] = datetime.fromisoformat(user_dict["birthday"])

    # Insert into the users collection (this is synchronous)
    db.users.insert_one(user_dict)

    return {"message": "User created successfully"}

# User login route
@auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Find the user by username
    user = db.users.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Create the JWT token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

# # User signup route
# @auth_router.post("/signup")
# async def signup(user: User):
#     # Check if the username already exists
#     existing_user = await db.users.find_one({"username": user.username})
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
    
#     # Check if the email already exists
#     existing_email = await db.users.find_one({"email": user.email})
#     if existing_email:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     # Hash the password and store the user in the database
#     hashed_password = get_password_hash(user.password)
    
#     # Prepare user data to store in the database
#     user_dict = user.dict()
#     user_dict["hashed_password"] = hashed_password
#     del user_dict["password"]  # Remove plaintext password

#     # Ensure the birthday is in the correct format
#     if isinstance(user_dict.get("birthday"), str):
#         # Parse the string date to a datetime object
#         user_dict["birthday"] = datetime.fromisoformat(user_dict["birthday"])

#     # Insert into the users collection
#     await db.users.insert_one(user_dict)

#     return {"message": "User created successfully"}

# # User login route
# @auth_router.post("/login")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     # Find the user by username
#     user = await db.users.find_one({"username": form_data.username})
#     if not user or not verify_password(form_data.password, user["hashed_password"]):
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     # Create the JWT token
#     access_token_expires = timedelta(minutes=30)
#     access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)

#     return {"access_token": access_token, "token_type": "bearer"}