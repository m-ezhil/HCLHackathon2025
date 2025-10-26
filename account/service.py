from .model import Account
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def create_account(db:Session, customer_id: int, account_type: str, amount: int):
    if amount < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Initial deposit cannot be negative")

    if account_type.upper() not in ["SAVINGS", "CURRENT", "FD"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid account type")
    
    if db.query(Account).filter((Account.customer_id == customer_id) & (Account.account_type == account_type)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account type already exists for this customer")

    new_account = Account(customer_id=customer_id, account_type=account_type, balance=amount)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account