from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.core import get_db
from customer.model import Customer
from auth.service import verify_access_token
from .schema import TransactionCreateSchema, TransactionResponseSchema
from .service import create_transaction_by_account_id, create_transaction_by_account_no, get_transaction_by_customer

router = APIRouter(prefix="/trans", tags=["Transaction"])

@router.post("/create", response_model=TransactionResponseSchema)
def transaction_creation(transaction: TransactionCreateSchema, db: Session = Depends(get_db), customer: Customer = Depends(verify_access_token)):
    if transaction.transaction_type.upper() not in ["WITHDRAW", "DEPOSIT"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid transaction type. Must be 'WITHDRAW' or 'DEPOSIT'.")
    
    if transaction.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be greater than zero.")
    
    if transaction.account_no:
        new_transaction = create_transaction_by_account_no(db, transaction.account_no, transaction.transaction_type, transaction.amount)
    else:
        new_transaction = create_transaction_by_account_id(db, transaction.account_id, transaction.transaction_type, transaction.amount)

    return TransactionResponseSchema(
        transaction_no=new_transaction.transaction_no,
        transaction_type=new_transaction.transaction_type,
        amount=new_transaction.amount,
        balance=new_transaction.balance
    )

@router.get("/", response_model=list[TransactionResponseSchema])
def get_transactions(db: Session = Depends(get_db), customer: Customer = Depends(verify_access_token)):
    transactions = get_transaction_by_customer(db, customer.id)
    return [TransactionResponseSchema(
        transaction_no=tx.transaction_no,
        transaction_type=tx.transaction_type,
        amount=tx.amount,
        balance=tx.balance
    ) for tx in transactions]