from sqlalchemy.orm import Session
from models import User, Room, Message
# When saving a message
def save_message(db: Session, room_name: str, username: str, content: str):
    room = db.query(Room).filter(Room.name == room_name).first()
    if not room:
        # Optionally create the room if it does not exist
        room = Room(name=room_name)
        db.add(room)
        db.commit()
        db.refresh(room)

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise Exception("User not found")

    message = Message(room_id=room.id, sender_id=user.id, content=content)
    db.add(message)
    db.commit()
    return message
