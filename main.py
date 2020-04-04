# main.py

from fastapi import FastAPI

from typing import Dict
from pydantic import BaseModel

app = FastAPI()
app.counter = 0

class PatientRq(BaseModel):
	name: str
	surename: str
class PatientIdResp(BaseModel):
	id: int
	patient: Dict

@app.get("/")
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}

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
	app.counter+=1
	return PatientIdResp(id=app.counter, patient=rq.dict())


