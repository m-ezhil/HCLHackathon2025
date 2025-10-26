from pydantic import BaseModel

class AccountCreateSchema(BaseModel):
    account_type: str
    initial_deposit: int

class AccountResponseSchema(BaseModel):
    id: int
    account_no: str
    account_type: str
    balance: int

    class Config:
        orm_mode = True