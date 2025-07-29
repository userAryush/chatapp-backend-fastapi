# test_main.py
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws/{room_id}")
async def websocket_chat(websocket: WebSocket, room_id: str):
    await websocket.accept()
    await websocket.send_text(f"You joined room: {room_id}")
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Echo: {data}")
