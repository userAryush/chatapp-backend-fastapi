from datetime import datetime
from database import SessionLocal
from models import Message, User  # Import User model
from fastapi import WebSocket, WebSocketDisconnect
from jose import JWTError
from auth import decode_token
from models import Room
connections = {}

async def websocket_endpoint(websocket: WebSocket, room_id: str, token: str, cursor: str = None):
    try:
        payload = decode_token(token)
        username = payload["sub"]
    except JWTError:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    db = SessionLocal()
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        new_room = Room(id=room_id, name=f"Room {room_id}")
        db.add(new_room)
        db.commit()
    db.close()
    if room_id not in connections:
        connections[room_id] = []
    connections[room_id].append(websocket)

    

    # Fetch user from DB once here using username
    user = db.query(User).filter(User.username == username).first()
    if not user:
        await websocket.close(code=1008)
        db.close()
        return

    # Parse cursor datetime if provided
    if cursor:
        try:
            cursor_dt = datetime.fromisoformat(cursor)
        except ValueError:
            cursor_dt = None
    else:
        cursor_dt = None

    # Fetch messages with cursor-based pagination
    query = db.query(Message).filter(Message.room_id == room_id)
    if cursor_dt:
        query = query.filter(Message.timestamp < cursor_dt)
    recent_messages = query.order_by(Message.timestamp.desc()).limit(20).all()

    # Send messages oldest first
    for msg in reversed(recent_messages):
        await websocket.send_text(f"[{msg.timestamp.strftime('%H:%M')}] {msg.sender.username}: {msg.content}")

    db.close()

    try:
        while True:
            data = await websocket.receive_text()
            timestamp = datetime.utcnow()

            # Store message
            db = SessionLocal()
            message = Message(
                room_id=room_id,
                content=data,
                sender_id=user.id,   # use sender_id here (integer FK)
                timestamp=timestamp
            )
            db.add(message)
            db.commit()
            db.close()

            # Broadcast to all in room
            for conn in connections[room_id]:
                await conn.send_text(f"[{timestamp.strftime('%H:%M')}] {username}: {data}")

    except WebSocketDisconnect:
        connections[room_id].remove(websocket)
