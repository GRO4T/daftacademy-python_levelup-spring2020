from pydantic import BaseModel
import database as db
from fastapi import Response, HTTPException, status, APIRouter
import sqlite3

router = APIRouter()

class Album(BaseModel):
    title: str
    artist_id: int

@router.post("/albums")
async def add_album(response: Response, album: Album):
    artistWithId = db.connection.execute("SELECT Name FROM artists WHERE ArtistId=?", (album.artist_id, )).fetchone()
    if (artistWithId == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "No artist with given id"}
        )
    cursor = db.connection.execute("INSERT INTO albums (Title, ArtistId) VALUES (?,?)", (album.title, album.artist_id, ))
    db.connection.commit()
    new_album_id = cursor.lastrowid
    db.connection.row_factory = sqlite3.Row
    album = db.connection.execute("SELECT * FROM albums WHERE AlbumId=?", (new_album_id, )).fetchone()
    response.status_code = status.HTTP_201_CREATED
    return album

@router.get("/albums/{album_id}")
async def get_album(response: Response, album_id: int):
    db.connection.row_factory = sqlite3.Row
    album = db.connection.execute("SELECT * FROM albums WHERE AlbumId=?", (album_id, )).fetchone()
    if (album == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "No album with given id"}
        )
    response.status_code = status.HTTP_200_OK
    return album
