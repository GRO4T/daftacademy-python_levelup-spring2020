from pydantic import BaseModel
import database as db
from fastapi import Response, HTTPException, status, APIRouter
import sqlite3

router = APIRouter()

class Customer(BaseModel):
    company: str = None
    address: str = None
    city: str = None
    state: str = None
    country: str = None
    postalcode: str = None
    fax: str = None

@router.put("/customers/{customer_id}")
async def update_customer(response: Response, customer_id: int, fields_to_update: Customer):
    db.connection.row_factory = sqlite3.Row
    stored_customer = db.connection.execute("SELECT * FROM customers WHERE CustomerId=?", (customer_id, )).fetchone()
    if (stored_customer == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "No customer with given id"}
        )
    stored_customer = {k.lower(): v for k, v in dict(stored_customer).items()}
    stored_customer_model = Customer(**stored_customer)
    update_data = fields_to_update.dict(exclude_unset=True)
    updated_customer = stored_customer_model.copy(update=update_data)

    cursor = db.connection.execute(
        "UPDATE customers SET Company=?, Address=?, City=?, "
        "State=?, Country=?, PostalCode=?, Fax=? WHERE CustomerId=?", (updated_customer.company,
                                                                     updated_customer.address,
                                                                     updated_customer.city,
                                                                     updated_customer.state,
                                                                     updated_customer.country,
                                                                     updated_customer.postalcode,
                                                                     updated_customer.fax,
                                                                     customer_id, ))
    db.connection.commit()
    customer = db.connection.execute("SELECT * FROM customers WHERE CustomerId=?", (customer_id, )).fetchone()
    response.status_code = status.HTTP_200_OK
    return customer
