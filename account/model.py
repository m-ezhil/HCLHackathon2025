from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, event
from database.core import Base
from datetime import datetime

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    account_no = Column(String, unique=True)
    account_type = Column(String, nullable=False)
    balance = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    def __init__(self, customer_id: int, account_type: str, balance: int = 0):
        self.customer_id = customer_id
        self.account_type = account_type
        self.balance = balance
        self.created_at = datetime.now()

@event.listens_for(Account, "after_insert")
def generate_account_no(mapper, connection, target):
    account_no = f"ACC{str(target.id).zfill(9)}"
    connection.execute(
        Account.__table__.update()
        .where(Account.id == target.id)
        .values(account_no=account_no)
    )