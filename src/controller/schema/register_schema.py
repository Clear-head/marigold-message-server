from datetime import datetime
from pydantic import BaseModel

class RegisterSchema(BaseModel):
    username: str
    password: str
    email: str
    phone_number: str
    birth_date: datetime
    gender: bool
    
