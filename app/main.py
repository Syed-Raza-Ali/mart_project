from fastapi import FastAPI
from sqlmodel import Session
from app.user_model import User 
from app.db_connector import create_db_and_tables, get_session
# add FastAPI to create routes
app = FastAPI() 

@app.get('/')
def root_route():
    return {"message": "Hello, FastAPI!"}

# def add_user_into_db(user_base : User, session : Session):
    