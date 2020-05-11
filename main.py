# main.py

import sqlite3

from hashlib import sha256

from fastapi import FastAPI, HTTPException, Depends, Cookie, status, Request, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

from routers import sales, customers, albums, tracks

import database as db

from typing import Dict
from pydantic import BaseModel

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schemas import Artist
from models import OrmArtist
from database import SessionLocal

app = FastAPI()
app.next_patient_id = 0
app.patient_dict = {}
app.sessions = {}
app.secret_key = "very constatn and random secret, best 64 characters"

templates = Jinja2Templates(directory="templates")

security = HTTPBasic()

app.include_router(sales.router)
app.include_router(customers.router)
app.include_router(albums.router)
app.include_router(tracks.router)

@app.on_event("startup")
async def startup():
    db.connection = sqlite3.connect("chinook.db")
    app.db = SessionLocal()

@app.on_event("shutdown")
async def shutdown():
    db.connection.close()
    app.db.close()

def check_login(session_token: str = Cookie(None)):
    if session_token not in app.sessions:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorised"
        )

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/welcome")
def welcome(request: Request, session_token: str = Depends(check_login)):
    return templates.TemplateResponse("welcome.html", {"request": request, "user": app.sessions[session_token]})

@app.post("/login")
def login(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if (credentials.username == "trudnY" and credentials.password == "PaC13Nt"):
        user = credentials.username
        password = credentials.password
        session_token = sha256(bytes(f"{user}{password}{app.secret_key}", encoding="utf-8")).hexdigest()
        if session_token not in app.sessions:
            app.sessions[session_token] = user

        response.set_cookie(key="session_token", value=session_token)
        response.headers["Location"] = "/welcome"
        response.status_code = status.HTTP_302_FOUND
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.post("/logout")
def logout(response: Response, session_token: str = Depends(check_login)):
    app.sessions.pop(session_token)
    response.headers["Location"] = "/"
    response.status_code = status.HTTP_302_FOUND

class Patient(BaseModel):
    name: str
    surname: str

@app.post("/patient")
def add_patient(response: Response, rq: Patient, session_token: str = Depends(check_login)):
    app.patient_dict[app.next_patient_id] = rq.dict()
    response.headers["Location"] = f"/patient/{str(app.next_patient_id)}"
    response.status_code = status.HTTP_302_FOUND
    app.next_patient_id += 1

@app.get("/patient")
def get_all_patients(response: Response, session_token: str = Depends(check_login)):
    return app.patient_dict

@app.get("/patient/{pk}", response_model=Patient)
def get_patient(response: Response, pk: int, session_token: str = Depends(check_login)):
    if pk not in app.patient_dict:
        raise HTTPException(status_code=204, detail="Item not found")
    return Patient(name=app.patient_dict[pk]["name"], surname=app.patient_dict[pk]["surname"])

@app.delete("/patient/{pk}")
def delete_patient(response: Response, pk: int, session_token: str = Depends(check_login)):
    if pk not in app.patient_dict:
        raise HTTPException(status_code=404, detail="Item not found")
    app.patient_dict.pop(pk)
    response.status_code = status.HTTP_204_NO_CONTENT

@app.get("/method")
@app.post("/method")
@app.delete("/method")
@app.put("/method")
def get_method(request: Request):
    return {"method":str(request.method)}

@app.get("/artists/{artist_id}", response_model=Artist)
async def get_artist(artist_id: int):
    db_artist = app.db.query(OrmArtist).filter(OrmArtist.artist_id == artist_id).first()
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return db_artist
