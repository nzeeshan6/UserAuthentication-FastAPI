from datetime import datetime, timedelta
from jose import JWTError, jwt
from database.model import activeUser

SECRET_KEY = "5f79568f06a5fb8009011e5d9e39e7ee217482cbd71a3bf481724d98406de43d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def store_access_token(jwtToken:str, jwtEmail:str):
    result = activeUser.fetch({'email':jwtEmail})
    if result.count==0:
        activeUser.put({'email':jwtEmail, 'token':jwtToken})
    else:
        key = result.items[0].get('key')
        activeUser.update({'token':jwtToken},key)

def validate_access_token(jwtToken: str):
    decodedJWT = {}
    try:
        decodedJWT = jwt.decode(jwtToken, SECRET_KEY, algorithms= ALGORITHM)
    finally:
        jwtEmail = decodedJWT.get("sub")
        if jwtEmail == None:
            return "404"
            
        if jwtEmail:
            result = activeUser.fetch({'email':jwtEmail, 'token': jwtToken})
            if result.count==1:
                return jwtEmail   
            else:
                return "404"
    
        