import sqlite3
import json
import asyncio
import os
import random
from datetime import datetime
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Stadium Smart Experience")

# Static files aur CORS setup
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DB_NAME = "events.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Tables creation logic
    cursor.execute("CREATE TABLE IF NOT EXISTS zones (id INTEGER PRIMARY KEY, name TEXT, section TEXT, current_capacity INTEGER, max_capacity INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, customer_name TEXT, item_name TEXT, status TEXT DEFAULT 'pending')")
    # Initial data entry
    cursor.execute("SELECT COUNT(*) FROM zones")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO zones (name, section, current_capacity, max_capacity) VALUES ('North Gate', 'Entry', 20, 100)")
    conn.commit()
    conn.close()

init_db()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Simulate crowd density every 10 seconds
            await asyncio.sleep(10)
            data = {"type": "crowd_update", "density": random.randint(10, 90)}
            await websocket.send_json(data)
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
