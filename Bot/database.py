from models import User, Expense
from config import engine, Base

from contrib import *


def init_db():
    Base.metadata.create_all(bind=engine)
    good('DB is inizilised!')

def drop_db():
    Base.metadata.drop_all(bind=engine)
    good('DB is dropped!')
