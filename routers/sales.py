from fastapi import APIRouter, Response, HTTPException, status
import database as db
import sqlite3

router = APIRouter()

def get_sales_by_customer():
    db.connection.row_factory = sqlite3.Row
    customer_expenses = db.connection.execute("SELECT c.CustomerId, c.Email, c.Phone, cs.Sum "
                                                "FROM customers c JOIN "
                                                "(SELECT CustomerId, Round(Sum(Total), 2) Sum FROM invoices "
                                                "GROUP BY CustomerId) cs "
                                                "ON c.CustomerId = cs.CustomerId "
                                                "ORDER BY cs.Sum DESC, c.CustomerId").fetchall()
    return customer_expenses

def get_sales_by_genre():
    db.connection.row_factory = sqlite3.Row
    sales_by_genre = db.connection.execute(
                                        "SELECT g.Name, sg.Sum FROM genres g "
                                        "JOIN "
                                        "(SELECT Sum(ii.Quantity) Sum, t.GenreId FROM invoice_items ii "
                                        "JOIN tracks t on t.TrackId = ii.TrackId "
                                        "GROUP BY t.GenreId) sg "
                                        "ON sg.GenreId = g.GenreId "
                                        "ORDER BY Sum DESC, Name").fetchall()
    return sales_by_genre

@router.get("/sales")
async def get_sales(response: Response, category: str):
    if (category == "customers"):
        return get_sales_by_customer()
    elif (category == "genres"):
        return get_sales_by_genre()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "No category of stats with given name"}
        )
