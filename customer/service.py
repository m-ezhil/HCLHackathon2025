from fastapi import HTTPException, status
from auth.utils import hash_password, is_password_strong
from customer.model import Customer
from sqlalchemy.orm import Session
import re

def create_customer(db:Session, name: str, email: str, password: str, pan_no: str):
    hashed_password = hash_password(password)
    
    new_customer = Customer(name=name, email=email, hashed_password=hashed_password, pan_no=pan_no)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

def get_customer_by_email(db:Session, email: str):
    return db.query(Customer).filter(Customer.email == email).first()

def get_customer_by_pan(db:Session, pan_no: str):
    return db.query(Customer).filter(Customer.pan_no == pan_no).first()