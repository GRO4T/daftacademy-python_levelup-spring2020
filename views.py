from schemas import Artist
from models import OrmArtist

@app.on_event("startup")
async def startup():
    app.db = SessionLocal()


@app.on_event("shutdown")
async def shutdown():
    app.db.close()

@app.get("/artists/{artist_id}", response_model=Artist)
async def get_artist(artist_id: int):
    db_artist = app.db.query(OrmArtist).filter(OrmArtist.artist_id == artist_id).first()
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return db_artist
