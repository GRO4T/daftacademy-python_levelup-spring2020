# main.py

import sqlite3

from hashlib import sha256

from fastapi import FastAPI, HTTPException, Depends, Cookie, status, Request, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

from typing import Dict
from pydantic import BaseModel

app = FastAPI()
app.next_patient_id = 0
app.patient_dict = {}
app.sessions = {}
app.secret_key = "very constatn and random secret, best 64 characters"

templates = Jinja2Templates(directory="templates")

security = HTTPBasic()

@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("chinook.db")

@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()

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

@app.get("/tracks")
async def get_tracks(response: Response, page: int = 0, per_page: int = 10):
    app.db_connection.row_factory = sqlite3.Row
    tracks = app.db_connection.execute("SELECT * FROM tracks ORDER BY TrackId "
                                       "LIMIT ? OFFSET ?", (per_page, page*per_page, )).fetchall()
    response.status_code = status.HTTP_200_OK
    return tracks

@app.get("/tracks/composers")
async def get_composer_tracks(response: Response, composer_name: str):
    tracknames = app.db_connection.execute("SELECT Name FROM tracks WHERE Composer=? ORDER BY Name", (composer_name, )).fetchall()
    if (tracknames == []):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "No such composer"}
        )
    response.status_code = status.HTTP_200_OK
    return [x[0] for x in tracknames]

class Album(BaseModel):
    title: str
    artist_id: int

@app.post("/albums")
async def add_album(response: Response, album: Album):
    artistWithId = app.db_connection.execute("SELECT Name FROM artists WHERE ArtistId=?", (album.artist_id, )).fetchone()
    if (artistWithId == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "No artist with given id"}
        )
    cursor = app.db_connection.execute("INSERT INTO albums (Title, ArtistId) VALUES (?,?)", (album.title, album.artist_id, ))
    app.db_connection.commit()
    new_album_id = cursor.lastrowid
    app.db_connection.row_factory = sqlite3.Row
    album = app.db_connection.execute("SELECT * FROM albums WHERE AlbumId=?", (new_album_id, )).fetchone()
    response.status_code = status.HTTP_201_CREATED
    return album

@app.get("/albums/{album_id}")
async def get_album(response: Response, album_id: int):
    app.db_connection.row_factory = sqlite3.Row
    album = app.db_connection.execute("SELECT * FROM albums WHERE AlbumId=?", (album_id, )).fetchone()
    if (album == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "No album with given id"}
        )
    response.status_code = status.HTTP_200_OK
    return album

class Customer(BaseModel):
    company: str = None
    address: str = None
    city: str = None
    state: str = None
    country: str = None
    postalcode: str = None
    fax: str = None
"""
def createCustomerUpdateString(stored_customer: sqlite3.Row, fields_to_update: Customer):
    stored_customer = {k.lower(): v for k, v in dict(stored_customer).items()}
    stored_customer_model = Customer(**stored_customer)
    update_data = fields_to_update.dict(exclude_unset=True)
    updated_customer = stored_customer_model.copy(update=update_data)
    return str(updated_customer).replace(" ", ", ")
"""
@app.put("/customers/{customer_id}")
async def update_customer(response: Response, customer_id: int, fields_to_update: Customer):
    app.db_connection.row_factory = sqlite3.Row
    stored_customer = app.db_connection.execute("SELECT * FROM customers WHERE CustomerId=?", (customer_id, )).fetchone()
    if (stored_customer == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "No customer with given id"}
        )
    stored_customer = {k.lower(): v for k, v in dict(stored_customer).items()}
    stored_customer_model = Customer(**stored_customer)
    update_data = fields_to_update.dict(exclude_unset=True)
    updated_customer = stored_customer_model.copy(update=update_data)

    cursor = app.db_connection.execute(
        "UPDATE customers SET Company=?, Address=?, City=?, "
        "State=?, Country=?, PostalCode=?, Fax=? WHERE CustomerId=?", (updated_customer.company,
                                                                     updated_customer.address,
                                                                     updated_customer.city,
                                                                     updated_customer.state,
                                                                     updated_customer.country,
                                                                     updated_customer.postalcode,
                                                                     updated_customer.fax,
                                                                     customer_id, ))
    app.db_connection.commit()
    customer = app.db_connection.execute("SELECT * FROM customers WHERE CustomerId=?", (customer_id, )).fetchone()
    response.status_code = status.HTTP_200_OK
    return customer


def handle_customers():
    app.db_connection.row_factory = sqlite3.Row
    customer_expenses = app.db_connection.execute("SELECT c.CustomerId, c.Email, c.Phone, cs.Sum "
                                                "FROM customers c JOIN "
                                                "(SELECT CustomerId, Round(Sum(Total), 2) Sum FROM invoices "
                                                "GROUP BY CustomerId) cs "
                                                "ON c.CustomerId = cs.CustomerId "
                                                "ORDER BY cs.Sum DESC, c.CustomerId").fetchall()
    return customer_expenses

def handle_genres():
    app.db_connection.row_factory = sqlite3.Row
    sales_by_genre = app.db_connection.execute(
                                        "SELECT g.Name, sg.Sum FROM genres g "
                                        "JOIN "
                                        "(SELECT Sum(ii.Quantity) Sum, t.GenreId FROM invoice_items ii "
                                        "JOIN tracks t on t.TrackId = ii.TrackId "
                                        "GROUP BY t.GenreId) sg "
                                        "ON sg.GenreId = g.GenreId "
                                        "ORDER BY Sum DESC, Name").fetchall()
    return sales_by_genre

@app.get("/sales")
async def get_sales(response: Response, category: str):
    if (category == "customers"):
        return handle_customers()
    elif (category == "genres"):
        return handle_genres()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "No category of stats with given name"}
        )

