from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .service import create_account
from .schema import AccountCreateSchema, AccountResponseSchema
from database.core import get_db
from auth.service import verify_access_token
from customer.model import Customer
from transaction.service import create_transaction


router = APIRouter(prefix="/account", tags=["Account"])

@router.post("/create", response_model=AccountResponseSchema)
def account_creation(account: AccountCreateSchema, customer: Customer = Depends(verify_access_token), db: Session = Depends(get_db)):
    new_account = create_account(db, customer.id, account.account_type, account.initial_deposit)
    create_transaction(db, new_account.id, "DEPOSIT", account.initial_deposit)
    return new_account
