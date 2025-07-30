# 🗨️ FastAPI Realtime Chat Application

A simple, **role-based real-time chat** application built using **FastAPI**, **WebSockets**, and **MySQL**.  
Supports **JWT-based authentication**, **admin/user role access control**, and **room-based chat** with message persistence.

---
## API Documentation
https://documenter.getpostman.com/view/38648701/2sB3B8qsip
## Chat Screenshots

### Sample Chat Conversation

![Chat Screenshot 1](screenshots/chat1.png)

## 🚀 Features

✅ User Signup/Login with hashed passwords  
✅ JWT Authentication  
✅ Role-based Access Control (RBAC)  
✅ Real-time chat via WebSocket  
✅ Room-based messaging  
✅ Message history with cursor-based pagination  
✅ Admin-only route access  

---

## 🛠️ Tech Stack

- **Backend**: FastAPI  
- **Authentication**:
  - JWT (`python-jose`)
  - Password hashing (`passlib`)
- **Database**: MySQL with SQLAlchemy ORM  
- **Realtime Communication**: WebSocket  
- **Client Testing**: Postman 

---

## 🌐 WebSocket Chat

### URL Format
ws://localhost:8000/ws/{room_id}?token=<JWT>


### How It Works
- Authenticates user using the provided JWT token.
- Joins the specified chat room.
- Sends the **last 20 messages** from the room history upon connection.
- Broadcasts new messages to all connected users in the room in real-time.

---

### 🧪 Sample Workflow

1. Register or login via the `/signup` and `/login` endpoints.
2. Copy the JWT token from the login response.
3. Use a WebSocket client (e.g., Postman) to connect:
4. Start chatting in real-time with other users in the room!


