from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from customer.service import get_customer_by_email, create_customer
from database.core import get_db
from customer.service import get_customer_by_pan, get_customer_by_email
from .utils import hash_password, verify_password
from .service import create_access_token, verify_access_token
from .schema import Token, LoginRequest, LoginResponse, SignupRequest

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(login_request: LoginRequest, db=Depends(get_db)):
    customer = get_customer_by_email(db, login_request.email)
    if not customer or not verify_password(login_request.password, customer.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    access_token = create_access_token(data={"sub": customer.email})
    return Token(access_token=access_token, token_type="bearer")

@router.post("/signup", response_model=LoginResponse)
def signup(signup_request: SignupRequest, db=Depends(get_db)):
    existing_email = get_customer_by_email(db, signup_request.email)
    existing_pan = get_customer_by_pan(db, signup_request.pan_no)
    if existing_pan:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PAN No already exists")
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    create_customer(db, signup_request.name, signup_request.email, signup_request.password, signup_request.pan_no)
    return LoginResponse(message="Customer registered successfully")