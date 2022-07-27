from graphlib import CycleError
from passlib.context import CryptContext
import rsa

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encrypt(password: str):
    return context.hash(password)

def verify(password: str, hashedPassword:str):
    return context.verify(password, hashedPassword)

def encryptWithKey(token:str, key: str):
    return rsa.encrypt(token.encode(), key)

