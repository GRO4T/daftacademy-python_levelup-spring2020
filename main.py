# main.py

from hashlib import sha256
from fastapi import FastAPI, HTTPException, Depends, Cookie, status
from starlette.responses import RedirectResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from typing import Dict
from pydantic import BaseModel

app = FastAPI()
app.counter = 0
app.patient_dict = {}
app.sessions = []

security = HTTPBasic()

app.secret_key = "very constatn and random secret, best 64 characters"

class PatientRq(BaseModel):
    name: str
    surename: str

class PatientIdResp(BaseModel):
    id: int
    patient: Dict

class GetPatientResp(BaseModel):
    name: str
    surename: str

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/welcome")
def welcome():
    return {"message": "Welcome to my page!"}

@app.post("/login")
def login(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if (credentials.username == "trudnY" and credentials.password == "PaC13Nt"):
        user = credentials.username
        password = credentials.password
        session_token = sha256(bytes(f"{user}{password}{app.secret_key}", encoding="utf-8")).hexdigest()
        if session_token not in app.sessions:
            app.sessions.append(session_token)
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
def logout(*, response: Response, session_toker: str = Cookie(None)):
    if session_token not in app.sessions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorised"
        )
    else:
        app.sessions.remove(session_toker)
        response.headers["Location"] = "/welcome"
        response.status_code = status.HTTP_302_FOUND

@app.get("/method")
def get_method():
    return {"method": "GET"}

@app.post("/method")
def post_method():
    return {"method": "POST"}

@app.delete("/method")
def delete_method():
    return {"method": "DELETE"}

@app.put("/method")
def put_method():
    return {"method": "PUT"}

@app.post("/patient", response_model=PatientIdResp)
def get_patient_id(rq: PatientRq, session_toker: str = Cookie(None)):
    if session_token not in app.sessions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorised"
        )
    app.patient_dict[app.counter] = rq.dict()
    app.counter+=1
    return PatientIdResp(id=app.counter, patient=rq.dict())

@app.get("/patient/{pk}", response_model=GetPatientResp)
def get_patient(pk: int):
    if pk not in app.patient_dict:
        raise HTTPException(status_code=204, detail="Item not found")
    return GetPatientResp(name=app.patient_dict[pk]["name"], surename=app.patient_dict[pk]["surename"])
