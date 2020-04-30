import database as db
from fastapi import Response, HTTPException, status, APIRouter
import sqlite3

router = APIRouter()

@router.get("/tracks")
async def get_tracks(response: Response, page: int = 0, per_page: int = 10):
    db.connection.row_factory = sqlite3.Row
    tracks = db.connection.execute("SELECT * FROM tracks ORDER BY TrackId "
                                       "LIMIT ? OFFSET ?", (per_page, page*per_page, )).fetchall()
    response.status_code = status.HTTP_200_OK
    return tracks

@router.get("/tracks/composers")
async def get_composer_tracks(response: Response, composer_name: str):
    tracknames = db.connection.execute("SELECT Name FROM tracks WHERE Composer=? ORDER BY Name", (composer_name, )).fetchall()
    if (tracknames == []):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "No such composer"}
        )
    response.status_code = status.HTTP_200_OK
    return [x[0] for x in tracknames]
