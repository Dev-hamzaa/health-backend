# from typing import union
from fastapi import FastAPI
from pydantic import BaseModel
from app.routes import doctor_router

app=FastAPI();




@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(doctor_router)
