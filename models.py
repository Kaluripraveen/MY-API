from pydantic import BaseModel

class UserRegistration(BaseModel):
    username: str
    email: str
    full_name: str
    password: str

class UserProfile(BaseModel):
    username: str
    full_name: str
    email: str

class UserLogin(BaseModel):
    email: str
    password: str  