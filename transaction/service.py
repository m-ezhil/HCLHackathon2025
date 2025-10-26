from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException, status
from account.model import Account
from .model import Transaction


def create_transaction(db: Session, account_id: int, transaction_type: str, amount: int) -> Transaction:
    account = db.query(Account).filter(Account.id == account_id).first()
    previous_balance: float = account.balance if account else 0

    if transaction_type.upper() == "DEPOSIT":
        account.balance += amount
    elif transaction_type.upper() == "WITHDRAW":
        if account.balance < amount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance for withdrawal.")
        account.balance -= amount

    transaction = Transaction(account_id=account_id, transaction_type=transaction_type, amount=amount, balance=previous_balance)
    db.add(transaction)

    db.commit()
    db.refresh(transaction)
    return transaction

def get_transaction_by_account(db: Session, account_id: int):
    return db.query(Transaction).filter(Transaction.account_id == account_id).order_by(desc(Transaction.created_at)).all()

def get_transaction_by_customer(db: Session, customer_id: int):
    return db.query(Transaction).join(Account).filter(Account.customer_id == customer_id).order_by(desc(Transaction.created_at)).all()