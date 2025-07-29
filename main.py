from fastapi import FastAPI, Depends, HTTPException, WebSocket
from database import Base, engine, SessionLocal
from models import User
from schemas import UserCreate, UserLogin
from auth import hash_password, verify_password, create_token
from sqlalchemy.orm import Session
from rbac import require_role
from websocket_handler import websocket_endpoint

# creating app
app = FastAPI()
# creates all database tables based on your SQLAlchemy models if they don't already exist.
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()  # Create a new DB session
    try:
        yield db          # Provide it to the request
    finally:
        db.close()        # Always close DB connection after request ends



# user: UserCreate → Incoming request body will be validated using Pydantic schema.
# db: Session = Depends(get_db) → Injects a DB session into this function.
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(400, detail="Username taken")
    hashed = hash_password(user.password)
    new_user = User(username=user.username, password=hashed, role=user.role)
    db.add(new_user)
    db.commit() # database ma ni save gareko
    return {"message": "User created"}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(401, detail="Invalid credentials")
    token = create_token({"sub": db_user.username, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/admin-only")
def admin_route(user=Depends(require_role("admin"))):
    return {"message": f"Welcome, admin {user['sub']}"}

@app.websocket("/ws/{room_id}")
async def websocket_chat(websocket: WebSocket, room_id: str):
    token = websocket.query_params.get("token")
    await websocket_endpoint(websocket, room_id, token)
    
