from fastapi import FastAPI
import sqlite3
import random

app = FastAPI()

def get_db():
    return sqlite3.connect("streams.db", check_same_thread=False)


@app.get("/streams")
def get_streams():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM streams")
    rows = cursor.fetchall()

    return [
        {
            "id": r[0],
            "streamer": r[1],
            "game": r[2],
            "viewers": r[3]
        }
        for r in rows
    ]


@app.get("/streams/{stream_id}")
def get_stream(stream_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM streams WHERE id=?", (stream_id,))
    row = cursor.fetchone()

    if not row:
        return {"error": "Stream not found"}

    # simulate live viewers change
    new_viewers = max(0, row[3] + random.randint(-5, 10))

    cursor.execute(
        "UPDATE streams SET viewers=? WHERE id=?",
        (new_viewers, stream_id)
    )
    conn.commit()

    return {
        "id": row[0],
        "streamer": row[1],
        "game": row[2],
        "viewers": new_viewers
    }