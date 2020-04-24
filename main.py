# main.py

from hashlib import sha256

from fastapi import FastAPI, HTTPException, Depends, Cookie, status, Request, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

from typing import Dict
from pydantic import BaseModel

app = FastAPI()
app.counter = 0
app.patient_dict = {}
app.sessions = {}
app.secret_key = "very constatn and random secret, best 64 characters"

templates = Jinja2Templates(directory="templates")

security = HTTPBasic()


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
def welcome(request: Request, session_token: str = Cookie(None)):
    if session_token not in app.sessions:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorised"
        )
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
def logout(response: Response, session_token: str = Cookie(None)):
    if session_token not in app.sessions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorised"
        )
    app.sessions.pop(session_token)
    response.headers["Location"] = "/"
    response.status_code = status.HTTP_302_FOUND

@app.get("/method")
@app.post("/method")
@app.delete("/method")
@app.put("/method")
def get_method(request: Request):
    return {"method":str(request.method)}

@app.post("/test")
def test(session_token: str = Cookie(None)):
    return {"session": session_token}

@app.post("/patient", response_model=PatientIdResp)
def add_patient(rq: PatientRq, session_token: str = Cookie(None)):
    if session_token not in app.sessions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorised"
        )
    app.patient_dict[app.counter] = rq.dict()
    app.counter+=1
    return PatientIdResp(id=app.counter, patient=rq.dict())

@app.get("/patient/{pk}", response_model=GetPatientResp)
def get_patient(pk: int, session_token: str = Cookie(None)):
    if session_token not in app.sessions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorised"
        )
    if pk not in app.patient_dict:
        raise HTTPException(status_code=204, detail="Item not found")
    return GetPatientResp(name=app.patient_dict[pk]["name"], surename=app.patient_dict[pk]["surename"])
