from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

class MessageCreate(BaseModel):
    content: str
    room_id: str
    sender: str


#  schemas define how data is validated when sent in requests or returned in responses. likeeee "How data looks in API input/output"