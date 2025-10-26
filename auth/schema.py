from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    message: str

class Token(BaseModel):
    access_token: str
    token_type: str

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    pan_no: str