from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):  # Inheriting from SQLAlchemy Base 
    __tablename__ = "users"  # in the actual database this table will be named users
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(200)) # will hash it so keeping space
    role = Column(String(20), default="user")

    messages = relationship("Message", back_populates="sender")
    # One-to-many : one user can send many messages
    # This lets you access all messages sent by the user: user.messages
    # back_populates="sender" refers to the 'sender' relationship in the Message model


class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text, nullable=True)

    messages = relationship("Message", back_populates="room")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)  # actual message
    timestamp = Column(DateTime, default=datetime.utcnow)

    room = relationship("Room", back_populates="messages")
    sender = relationship("User", back_populates="messages")

# Models defines how data is stored in the database.

# User and Message:

# User.messages: All messages sent by this user.
# Message.sender: The user who sent this message.

# Room adn Message:

# Room.messages: All messages in this room.
# Message.room: The room to which this message belongs.