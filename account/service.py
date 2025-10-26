from .model import Account
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def create_account(db:Session, customer_id: int, account_type: str, amount: int):
    new_account = Account(customer_id=customer_id, account_type=account_type, balance=amount)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

def is_account_exists(db:Session, customer_id: int, account_type: str):
    accounts = db.query(Account).filter((Account.customer_id == customer_id) & (Account.account_type == account_type)).first()
    return accounts is not None