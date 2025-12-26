from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from datetime import datetime, timedelta, UTC, timezone

from models import User, Expense, ExpenseCategory
from contrib import now, bad

class UserRepository:

    @staticmethod
    def get_or_create(db: Session, telegram_id: int, **kwargs):
        user = db.query(User).filter(User.telegram_id == telegram_id).first()

        if not user:
            user_data = {
                'telegram_id': telegram_id,
                'created_at': now(),
                'default_currency': 'RUB',
                **kwargs
            }
            user = User(**user_data)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    
    @staticmethod
    def get_user(db: Session, telegram_id: int):
        return db.query(User).filter(User.telegram_id == telegram_id).first()
    
    @staticmethod
    def set_total_budget(db: Session, telegram_id: int, total_budget_amount: float) -> bool:
        if total_budget_amount <= 0:
            return False
        
        user = UserRepository.get_user(db, telegram_id)
        if not user:
            return False
                                                                                                                                                                                                
        user.total_budget = total_budget_amount
        db.commit()
        db.refresh(user)
        return True
    
    @staticmethod
    def update_total_budget(db: Session, telegram_id: int, change_amount: float) -> bool:
        user = UserRepository.get_user(db, telegram_id)
        if not user:
            return False
        
        current_budget = user.total_budget or 0
        new_budget = current_budget + change_amount

        if new_budget < 0:
            return False
        
        user.total_budget = new_budget
        db.commit()
        db.refresh(user)

    @staticmethod
    def budget_remain(db: Session, telegram_id: int) -> float:
        user = UserRepository.get_user(db=db, telegram_id=telegram_id)

        return (user.total_budget or 0) - (ExpenseRepository.get_expenses_amount(db=db, telegram_id=telegram_id) or 0)
        

class ExpenseRepository:

    @staticmethod
    def get_expenses_amount(db: Session, telegram_id: int) -> float:  # for what this?
        user = UserRepository.get_user(db, telegram_id)
        if not user:
            return 0.0
        
        total = db.query(func.sum(Expense.amount))\
          .filter(Expense.user_id == user.id)\
          .scalar()
        
        return total or 0.0

    @staticmethod
    def add_expense(db: Session, telegram_id: int, amount: float, category: str, description: str = ''):
        user = UserRepository.get_user(db, telegram_id)

        if not user:
            raise ValueError(f"User with t-id {telegram_id} not exists")
        
        try:
            expense_category = ExpenseCategory(category.lower())
        except ValueError:
            expense_category = ExpenseCategory.OTHER

        expense = Expense(
            user_id=user.id,
            amount=amount,
            category=expense_category,
            description=description,
            date=now()
        )

        db.add(expense)
        db.commit()
        db.refresh(expense)

        return Expense

    @staticmethod
    def get_expenses(db: Session, telegram_id: int, category: str = None, limit: int = 10) -> list:
        user = UserRepository.get_user(db, telegram_id)

        if not user:
            return []

        if category:

            expenses = db.query(Expense)\
                .filter(Expense.user_id == user.id)\
                .filter(Expense.category == category)\
                .order_by(desc(Expense.date))\
                .limit(limit)\
                .all()
        else:
            expenses = db.query(Expense)\
                .filter(Expense.user_id == user.id)\
                .order_by(desc(Expense.date))\
                .limit(limit)\
                .all()

        return expenses
    
    @staticmethod
    def get_today_expenses(db: Session, telegram_id: int) -> list:
        user = UserRepository.get_user(db, telegram_id=telegram_id)

        if not user:
            return []
        
        now_UTC = datetime.now(UTC)
        today_start = datetime(now_UTC.year, now_UTC.month, now_UTC.day, tzinfo=timezone.utc)

        expenses = db.query(Expense)\
            .filter(Expense.user_id == user.id)\
            .filter(Expense.date >= today_start)\
            .order_by(desc(Expense.date))\
            .all()
        
        return expenses
    
    @staticmethod
    def get_total_in_category(db: Session, telegram_id: int, category: ExpenseCategory):
        user = UserRepository.get_user(db, telegram_id=telegram_id)

        if not user:
            return []

        expenses = db.query(Expense)\
            .filter(Expense.user_id == user.id)\
            .filter(Expense.category == category)\
            .order_by(desc(Expense.date))\
            .all()
        
        summed = sum(expense.amount for expense in expenses)

        return summed
    
    @staticmethod
    def get_total_in_allcategories(db: Session, telegram_id: int):
        user = UserRepository.get_user(db, telegram_id=telegram_id)

        if not user:
            return []

        expenses = db.query(Expense)\
            .filter(Expense.user_id == user.id)\
            .order_by(desc(Expense.date))\
            .all()
        
        summed = sum(expense.amount for expense in expenses)

        return summed
    
    @staticmethod
    def sum_in_each_category(db: Session, telegram_id: int):
        user = UserRepository.get_user(db, telegram_id=telegram_id)

        if not user:
            return []
        
        result = {}
        for c in ExpenseCategory:
            result[c.value] = ExpenseRepository.get_total_in_category(
                db=db,
                telegram_id=user.telegram_id,
                category=c
            )
        return result
    
    
    @staticmethod
    def get_total_today(db: Session, telegram_id: id):
        expenses = ExpenseRepository.get_today_expenses(db, telegram_id=telegram_id)
        total = sum(expense.amount for expense in expenses)
        return total
    
    @staticmethod
    def delete(db: Session, telegram_id: int, expense_id: int) -> bool:
        try:
            user = UserRepository.get_user(db=db, telegram_id=telegram_id)

            if not(user):
                bad(f'User with t-id {telegram_id} not exists')
                return 0

            expense = db.query(Expense)\
                .filter(Expense.id == expense_id)\
                .filter(Expense.user_id == user.id)\
                .first()
            if not (expense):
                bad(f'Expense with ID {expense_id} not found in user with t-id {telegram_id}')
                return 0
        
            db.delete(expense)
            db.commit()
            return True
        except Exception as e:
            bad(f'Error on deleting expense(id={expense_id}, user_id={user.id})')
            db.rollback()
            return False
        