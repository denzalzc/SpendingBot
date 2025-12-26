from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy import Enum

from datetime import datetime, timezone

from config import Base
from contrib import now

import enum

import secrets, string


def get_category(category: str):
    return([c for c in ExpenseCategory if c.value == category])[0]


def generate_password(length=8):
    """Генерация случайного пароля заданной длины"""
    alphabet = string.ascii_letters + string.digits  # буквы и цифры
    return ''.join(secrets.choice(alphabet) for _ in range(length))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=1)
    telegram_id = Column(Integer, nullable=0, index=1, unique=1)
    username = Column(String(100), nullable=1)
    first_name = Column(String(100), nullable=1)
    last_name = Column(String(100), nullable=1)
    created_at = Column(DateTime, default=lambda: now())

    spend_password = Column(String(100), default=generate_password)

    default_currency = Column(String(100), default="RUB")
    monthly_budget = Column(Float, nullable=1)
    total_budget = Column(Float, nullable=1)

    expenses = relationship('Expense', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
            return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})>"         


class ExpenseCategory(enum.Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    UTILITIES = "utilities"
    SHOPPING = "shopping"
    HEALTH = "health"
    EDUCATION = "education"
    OTHER = "other"

class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=1)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=0, index=1)
    user = relationship('User', back_populates='expenses')

    amount = Column(Float, nullable=0)
    category = Column(Enum(ExpenseCategory), nullable=1)
    description = Column(Text, nullable=1)
    created_at = Column(DateTime, default=now())

    currency = Column(String(100), default='RUB')
    date = Column(DateTime, default=now())

    def __repr__(self):
        return f"<Expense(id={self.id}, amount={self.amount}, category={self.category.value})>"
    
    def output(self):
         return f"[ID: {self.id}] {self.created_at.strftime("%d.%m.%y:%H:%M")}: {str(self.amount).replace('.0', '')} {self.currency}"
    def output_with_category(self):
         return f"[ID: {self.id}] {self.created_at.strftime("%d.%m.%y:%H:%M")}| {self.category.value or ""} | {str(self.amount).replace('.0', '')} {self.currency}"
    


    