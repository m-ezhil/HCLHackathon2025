from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .service import create_account, is_account_exists
from .schema import AccountCreateSchema, AccountResponseSchema
from database.core import get_db
from auth.service import verify_access_token
from customer.model import Customer
from transaction.service import create_transaction_by_account_id


router = APIRouter(prefix="/account", tags=["Account"])

@router.post("/create", response_model=AccountResponseSchema)
def account_creation(account: AccountCreateSchema, customer: Customer = Depends(verify_access_token), db: Session = Depends(get_db)):
    if account.initial_deposit < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Initial deposit must be greater than or equal to zero")

    if account.account_type.upper() not in ["SAVINGS", "CURRENT", "FD"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid account type")

    if is_account_exists(db, customer.id, account.account_type):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account type already exists for this customer")
    
    new_account = create_account(db, customer.id, account.account_type, 0)
    create_transaction_by_account_id(db, new_account.id, "DEPOSIT", account.initial_deposit)
    return new_account
