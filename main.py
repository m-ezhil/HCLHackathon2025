from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.core import Base, engine
from auth.routes import router as auth_router
from account.routes import router as account_router
from transaction.routes import router as transaction_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(account_router)
app.include_router(transaction_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
