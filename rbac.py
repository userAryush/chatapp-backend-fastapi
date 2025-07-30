from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from auth import decode_token


# extracts token from headers
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# checks JWT token from the request verifies it
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # this decode_token verifies the token and returns the user
        return decode_token(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(role: str):
    def wrapper(user=Depends(get_current_user)):
        # checks if the user role matches the required role send while calling require_role function
        if user.get("role") != role:
            raise HTTPException(status_code=403, detail=f"Access forbidden! Only {role} can access this route")
        return user
    return wrapper
