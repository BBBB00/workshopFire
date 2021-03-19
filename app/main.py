import uvicorn
from fastapi import FastAPI, Path, Query, HTTPException
from starlette.responses import JSONResponse
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from database.mongodb import MongoDB
from config.development import config
from model.room import createRoomModel, updateRoomModel

mongo_config = config["mongo_config"]
mongo_db = MongoDB(
    mongo_config["host"],
    mongo_config["port"],
    mongo_config["user"],
    mongo_config["password"],
    mongo_config["auth_db"],
    mongo_config["db"],
    mongo_config["collection"],
)
mongo_db._connect()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return JSONResponse(content={"nothing": "return"}, status_code=200)


@app.get("/rooms")
def get_rooms(
    sort_by: Optional[str] = None,
    order: Optional[str] = Query(None, min_length=3, max_length=4),
):

    try:
        result = mongo_db.find(sort_by, order)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    return JSONResponse(
        content={"data": result},
        status_code=200,
    )


@app.post("/rooms")
def create_rooms(room: createRoomModel):
    try:
        room_id = mongo_db.create(room)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    return JSONResponse(
        content={
            "data": {
                "room_id": room_id,
            },
        },
        status_code=201,
    )


@app.get("/rooms/{room_id}")
def get_students_by_id(room_id: str = Path(None, min_length=4, max_length=4)):
    try:
        result = mongo_db.find_one(room_id)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    if result is None:
        raise HTTPException(status_code=404, detail="Student Id not found !!")

    return JSONResponse(
        content={"data": result},
        status_code=200,
    )


@app.patch("/rooms/{room_id}")
def update_books(
    room: updateRoomModel,
    room_id: str = Path(None, min_length=4, max_length=4),
):
    print("Room", room)
    try:
        updated_room_id, modified_count = mongo_db.update(room_id, room)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    if modified_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Student Id: {updated_room_id} is not update want fields",
        )

    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                "student_id": updated_room_id,
                "modified_count": modified_count,
            },
        },
        status_code=200,
    )


@app.delete("/rooms/{room_id}")
def delete_book_by_id(room_id: str = Path(None, min_length=4, max_length=4)):
    try:
        deleted_room_id, deleted_count = mongo_db.delete(room_id)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    if deleted_count == 0:
        raise HTTPException(
            status_code=404, detail=f"Student Id: {deleted_room_id} is not Delete"
        )

    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                "student_id": deleted_room_id,
                "deleted_count": deleted_count,
            },
        },
        status_code=200,
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3002, reload=True)
