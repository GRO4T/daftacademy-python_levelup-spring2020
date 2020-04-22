# main.py

from fastapi import FastAPI, HTTPException, Depends
from starlette.responses import RedirectResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from typing import Dict
from pydantic import BaseModel

app = FastAPI()
app.counter = 0
app.patient_dict = {}

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
def welcome():
	return {"message": "Welcome to my page!"}

@app.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security)):
    if (credentials.username == "trudnY" and credentials.password == "PaC13Nt"):
        return RedirectResponse(url="/welcome")
    else:
        return Response("Wrong credentials", status_code=401)

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
def get_patient_id(rq: PatientRq):
	app.patient_dict[app.counter] = rq.dict()
	app.counter+=1
	return PatientIdResp(id=app.counter, patient=rq.dict())

@app.get("/patient/{pk}", response_model=GetPatientResp)
def get_patient(pk: int):
	if pk not in app.patient_dict:
		raise HTTPException(status_code=204, detail="Item not found")
	return GetPatientResp(name=app.patient_dict[pk]["name"], surename=app.patient_dict[pk]["surename"])
