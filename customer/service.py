from fastapi import HTTPException, status
from auth.utils import hash_password, is_password_strong
from customer.model import Customer
from sqlalchemy.orm import Session
import re

def create_customer(db:Session, name: str, email: str, password: str, pan_no: str):
    if not is_password_strong(password):
        print(password)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number")

    hashed_password = hash_password(password)

    if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$", pan_no):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid PAN number format")
    
    if db.query(Customer).filter(Customer.email == email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    if db.query(Customer).filter(Customer.pan_no == pan_no).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PAN number already registered")
    
    new_customer = Customer(name=name, email=email, hashed_password=hashed_password, pan_no=pan_no)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return 

def get_customer_by_email(db:Session, email: str):
    return db.query(Customer).filter(Customer.email == email).first()

def get_customer_by_pan(db:Session, pan_no: str):
    return db.query(Customer).filter(Customer.pan_no == pan_no).first()