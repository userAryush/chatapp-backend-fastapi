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
    
    if user.role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="Invalid role. Only 'admin' or 'user' userrole is allowed!")
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(staus_code=400, detail="Username taken")
    
    # hashes the password before saving it in db 
    hashed = hash_password(user.password)
    # creates a new user obj
    new_user = User(username=user.username, password=hashed, role=user.role)
    # adds the new user to the db
    db.add(new_user)
    db.commit() # finally saved in database ma ni save gareko
    if user.role == "admin":
        msg = "Admin Created"
    elif user.role == "user":
        msg = "User Created"
        
    additional_msg = "\nWelcome to Aryush chatapp! for next process please login and get the jwt token to start a chat"
    return {"message": msg+ additional_msg}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    
    # gets the user from db by matching thier username
    db_user = db.query(User).filter(User.username == user.username).first()
    # if didnt find the username or the password is incorrect to db passs then raise error
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # after successfull verification create token and send it as a response
    token = create_token({"sub": db_user.username, "role": db_user.role,"id":db_user.id})
    msg = "user this token in the header eg. Authorization   Bearer -token-"
    return {"access_token": token, "token_type": "bearer", "message": msg}


# admin only access
@app.get("/admin-only")
def admin_route(user=Depends(require_role("admin"))): # require role helps in only allowing admin to access this route whose logic is in rbac.py
    return {"message": f"Welcome, admin {user['sub']}"}



@app.websocket("/ws/{room_id}")# this route is to create or join the chat room
async def websocket_chat(websocket: WebSocket, room_id: str):
    # extracts the JWT token from the query parameters of the websocket url
    try:
        token = websocket.query_params.get("token")
        await websocket_endpoint(websocket, room_id, token)
    # websocket does not supports the authorization header in some client so sending it as a query parameter
    
    # Pass the websocket object, room_id, and token to another handler
    # This other function handles authentication, messaging,..
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close(code=1003)

    
