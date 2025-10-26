from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException, status
from account.model import Account
from .model import Transaction


def create_transaction_by_account_id(db: Session, account_id: int, transaction_type: str, amount: int) -> Transaction:
    account = db.query(Account).filter((Account.id == account_id) & (Account.is_active == True)).first()
    previous_balance: float = account.balance if account else 0

    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found.")

    if transaction_type.upper() == "DEPOSIT":
        account.balance += amount
    elif transaction_type.upper() == "WITHDRAW":
        if account.balance < amount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance for withdrawal.")
        account.balance -= amount

    transaction = Transaction(account_id=account_id, transaction_type=transaction_type, amount=amount, balance=previous_balance+amount)
    db.add(transaction)

    db.commit()
    db.refresh(transaction)
    return transaction

def create_transaction_by_account_no(db: Session, account_no: str, transaction_type: str, amount: int) -> Transaction:
    account = db.query(Account).filter((Account.account_no == account_no) & (Account.is_active == True)).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found.")
    return create_transaction_by_account_id(db, account.id, transaction_type, amount)

def get_transaction_by_account(db: Session, account_id: int):
    return db.query(Transaction).filter(Transaction.account_id == account_id).order_by(desc(Transaction.created_at)).all()

def get_transaction_by_customer(db: Session, customer_id: int):
    return db.query(Transaction).join(Account).filter(Account.customer_id == customer_id).order_by(desc(Transaction.created_at)).all()