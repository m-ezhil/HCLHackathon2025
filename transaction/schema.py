from pydantic import BaseModel

class TransactionCreateSchema(BaseModel):
    account_no: str
    transaction_type: str 
    amount: int

class TransactionResponseSchema(BaseModel):
    transaction_no: str
    transaction_type: str
    amount: int

class TransactionDetailSchema(BaseModel):
    transaction_no: str
    account_no: str
    transaction_type: str
    amount: int
    created_at: str
    is_active: bool

class TransactionListSchema(BaseModel):
    transactions: list[TransactionDetailSchema]