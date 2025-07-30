from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# import secrets
# import string

# def generate_secure_key(length: int = 32) -> str:
#     """
#     Generates a cryptographically secure random key.

#     Args:
#         length (int): The desired length of the key.

#     Returns:
#         str: The generated secure random key.
#     """
#     alphabet = string.ascii_letters + string.digits + string.punctuation
#     secure_key = ''.join(secrets.choice(alphabet) for i in range(length))
#     return secure_key
# print(generate_secure_key(35))
SECRET_KEY = "El[7ba/0*XpA\qF*em}Zyk~5A|!C&/A7>e["
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# returns a hashed password for user text password while creating users
def hash_password(password: str):
    return pwd_context.hash(password)

# to check the hashed password with user input password at the time of login
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
