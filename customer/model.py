from sqlalchemy import Column, Integer, String, Boolean, DateTime, event
from database.core import Base
from datetime import datetime


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_no = Column(String, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    pan_no = Column(String, nullable=False, unique=True)
    create_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    def __init__(self, name: str, email: str, hashed_password: str, pan_no: str):
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.pan_no = pan_no
        self.create_at = datetime.now()

@event.listens_for(Customer, "after_insert")
def generate_customer_no(mapper, connection, target):
    customer_no = f"CUST{str(target.id).zfill(9)}"
    connection.execute(
        Customer.__table__.update()
        .where(Customer.id == target.id)
        .values(customer_no=customer_no)
    )