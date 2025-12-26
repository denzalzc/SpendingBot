from django.shortcuts import render
from django.http import HttpResponse
from Bot.repository import UserRepository, Expense, ExpenseRepository, User, ExpenseCategory
from Bot.database import init_db
from Bot.config import SessionLocal


def get_category(category: ExpenseCategory):
    return([c.value for c in ExpenseCategory if c == category])[0]

class ExpenseView:
     def __init__(self, expense: Expense):
          self.id = expense.id
          self. amount = expense.amount
          self.category = get_category(expense.category)
          self.description = expense.description
          self.created_at = expense.created_at

def testor(request):
    return render(request, 'test.html')

def enter(request):
    return render(request, 'enter.html')

def spends(request):
    if request.method == 'GET':
        tid = request.GET.get('tgid')
        tpass = request.GET.get('tgpass')

        init_db()
        db = SessionLocal()

        user = UserRepository.get_user(db=db, telegram_id=tid)

        if str(user.telegram_id) == str(tid) and str(user.spend_password) == str(tpass):
            spends = ExpenseRepository.get_expenses(db=db, telegram_id=user.telegram_id)
            spends = [ExpenseView(expense) for expense in spends]   
            return render(
                request,
                'spends.html',
                {
                    'spends': spends,
                    'total_amount': UserRepository.budget_remain(db=db, telegram_id=user.telegram_id) or 0,
                    'categories': [c.value for c in ExpenseCategory]
                }
            )
        else:
            return HttpResponse('WROND ID OR PASSWORD')


        
