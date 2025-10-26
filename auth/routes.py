import re
from fastapi import APIRouter, Depends, HTTPException, status
from customer.service import get_customer_by_email, create_customer
from database.core import get_db
from customer.service import get_customer_by_pan, get_customer_by_email
from .utils import verify_password, is_password_strong
from .service import create_access_token
from .schema import Token, LoginRequest, LoginResponse, SignupRequest

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(login_request: LoginRequest, db=Depends(get_db)):
    customer = get_customer_by_email(db, login_request.email)
    if not customer or not verify_password(login_request.password, customer.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    access_token = create_access_token(data={"sub": customer.email})
    return Token(access_token=access_token, token_type="bearer")

@router.post("/signup", response_model=Token)
def signup(signup_request: SignupRequest, db=Depends(get_db)):
    existing_email = get_customer_by_email(db, signup_request.email)
    existing_pan = get_customer_by_pan(db, signup_request.pan_no)

    if not is_password_strong(signup_request.password):
        print(signup_request.password)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number")
    
    if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$", signup_request.pan_no):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid PAN number format")
    
    if existing_pan:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PAN No already exists")
    
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    create_customer(db, signup_request.name, signup_request.email, signup_request.password, signup_request.pan_no)
    access_token = create_access_token(data={"sub": signup_request.email})
    return Token(access_token=access_token, token_type="bearer")