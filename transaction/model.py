from database.core import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, event
from datetime import datetime

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    transaction_no = Column(String, unique=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    transaction_type = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    balance = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    def __init__(self, account_id: int, transaction_type: str, amount: int, balance: int = 0):
        self.account_id = account_id
        self.transaction_type = transaction_type.upper()
        self.amount = amount
        self.balance = balance
        self.created_at = datetime.now()

@event.listens_for(Transaction, "after_insert")
def generate_transaction_no(mapper, connection, target):
    transaction_no = f"TRN{str(target.id).zfill(9)}"
    connection.execute(
        Transaction.__table__.update()
        .where(Transaction.id == target.id)
        .values(transaction_no=transaction_no)
    )