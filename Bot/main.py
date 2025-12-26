from repository import UserRepository, ExpenseRepository
from models import ExpenseCategory
from telebot.types import Message
from config import SessionLocal, WEB_URL
from contrib import parse_user_message_addexpense, parse_user_message_showexpense, parse_user_message_deleteexpense, parse_user_message_totalexpense, parse_user_message_updatebudget
from database import init_db
from graphic import create_diag
import telebot


def get_category(category: str):
    return([c for c in ExpenseCategory if c.value == category])[0]

init_db()
db = SessionLocal()

def get_user_from_message(m: Message):
    up = m.from_user

    user = UserRepository.get_or_create(
        db=db,
        telegram_id=up.id,
        username=up.username,
        first_name=up.first_name,
        last_name=up.last_name,
    )
    return user

def get_user_tgid(message: Message):
    return message.from_user.id


def get_api_key() -> str:
    with open('apikey.txt', 'r') as file:
        return str(file.read()).strip()
    
bot = telebot.TeleBot(get_api_key())
print('Bot is up.')
    
def send_to_src(message_src: telebot.types.Message, text: str) -> None:
    bot.send_message(message_src.chat.id, text, parse_mode='html')

def reply_to_src(message_src: telebot.types.Message, text: str) -> None:
    bot.reply_to(message_src, text, parse_mode='html')


@bot.message_handler(commands=['web'])
def web_command(message: Message):
    user = get_user_from_message(m=message)

    send_to_src(
        message,
        f"Your spends is avaiable at\n{WEB_URL}spends/?tgid={user.telegram_id}&tgpass={user.spend_password}"
    )

1002609684
@bot.message_handler(commands=['start'])
def start_command(message: Message):
    user = get_user_from_message(m=message)

    send_to_src(message, f"Hi, {user.first_name}!\nUser /add for adding new spend\nSpend format is /add 99.99 category")
    send_to_src(message, f"Avaiable categories:\n{'\n'.join([c.value for c in ExpenseCategory])}")

@bot.message_handler(commands=['add'])
def add_command(message: str):
    
    user_data = parse_user_message_addexpense(message)
    user = get_user_from_message(m=message)

    if not(user_data):
        send_to_src(message, 'Wrong /add command data format!')
        return
    if user_data == 'categoryMistake':
        send_to_src(message, f'Category {user_data['category']} not exists')
        return

    ExpenseRepository.add_expense(
        db=db,
        telegram_id=user.telegram_id,
        amount=user_data['amount'],
        category=user_data['category']
    )
    send_to_src(message, 'Added.')
    

@bot.message_handler(commands=['password'])
def getps_command(message: Message):
    user = get_user_from_message(m=message)

    send_to_src(message, f"Your spend-password: {user.spend_password}")

@bot.message_handler(commands=['id'])
def getid_command(message: Message):
    user = get_user_from_message(m=message)

    send_to_src(message, f"Your telegram-id: {user.telegram_id}")
        
@bot.message_handler(commands=['show'])
def show_command(message: str):
    user_data = parse_user_message_showexpense(message)
    user = get_user_from_message(m=message)

    if not(user_data):
        send_to_src(message, 'Wrong /show command data format!')
        return
    if user_data == 'categoryMistake':
        send_to_src(message, f'Category {user_data['category']} not exists')
        return
    
    # cat and count
    if user_data['category'] and user_data['count']:
        expenses = ExpenseRepository.get_expenses(
            db=db,
            telegram_id=user.telegram_id,
            category=get_category(user_data['category']),
            limit=user_data['count']
        )
        print(expenses)
        output_text = f"{user_data['category']} spends:\n{'\n'.join([e.output() for e in expenses])}"
        send_to_src(message, output_text)
        return
    # only cat
    if user_data['category'] and not(user_data['count']):
        expenses = ExpenseRepository.get_expenses(
            db=db,
            telegram_id=user.telegram_id,
            category=get_category(user_data['category'])
        )
        output_text = f"{user_data['category']} spends:\n{'\n'.join([e.output() for e in expenses])}"
        send_to_src(message, output_text)
        return
    # only count   
    if not(user_data['category']) and user_data['count']:
        expenses = ExpenseRepository.get_expenses(
            db=db,
            telegram_id=user.telegram_id,
            limit=user_data['count']
        )
        output_text = f"Spends:\n{'\n'.join([e.output_with_category() for e in expenses])}"
        send_to_src(message, output_text)
        return
    # not cat not count
    if not(user_data['category']) and not(user_data['count']):
        expenses = ExpenseRepository.get_expenses(
            db=db,
            telegram_id=user.telegram_id,
        )
        output_text = f"Spends:\n{'\n'.join([e.output_with_category() for e in expenses])}"
        send_to_src(message, output_text)
        return
    
@bot.message_handler(commands=['delete'])
def del_command(message: str):
    user_data = parse_user_message_deleteexpense(message)
    user = get_user_from_message(m=message)

    if not(user_data):
        send_to_src(message, 'Wrong /delete command data format!')

    ExpenseRepository.delete(
        db=db,
        telegram_id=user.telegram_id,
        expense_id=user_data
    )
    send_to_src(message, f'Spend with {user_data} ID is deleted.')

@bot.message_handler(commands=['total'])
def total_command(message: str):
    user_data = parse_user_message_totalexpense(message)
    user = get_user_from_message(m=message)   
    print(user_data)

    if not(user_data):
        send_to_src(message, 'Wrong /total command data format!')
        return

    if user_data[0] == 'categoryMistake':
        send_to_src(message, f'Category {user_data[1]} not exists')
        return
    # total all
    if not(user_data[0]) and not(user_data[1]):
        sum = ExpenseRepository.get_total_in_allcategories(
            db=db,
            telegram_id=user.telegram_id,
        )
        send_to_src(message, f"Total is {str(sum).replace('.0', '')}")
        return
    # total in category
    if user_data[0]:
        category = get_category(user_data[0])
        sum = ExpenseRepository.get_total_in_category(
            db=db,
            telegram_id=user.telegram_id,
            category=category
        )
        send_to_src(message, f"Total {user_data[0]} is {str(sum).replace('.0', '')}")

@bot.message_handler(commands=['diag'])
def diag_command(message: Message):
    user = get_user_from_message(m=message)  

    sum_in_cats = (ExpenseRepository.sum_in_each_category(
        db=db,
        telegram_id=user.telegram_id,
    ))

    categories = sum_in_cats.keys()
    values = sum_in_cats.values()
    diag = create_diag(categories=categories, sum_of_category=values)

    bot.send_photo(message.chat.id, diag)

@bot.message_handler(commands=['budget'])
def budget_command(message: Message):
    user = get_user_from_message(m=message)
    send_to_src(message, f"Budged is - {user.total_budget} RUB")


@bot.message_handler(commands=['setbudget'])
def setbudget_command(message: Message):
    user = get_user_from_message(m=message)
    user_data = parse_user_message_updatebudget(m=message)

    if not(user_data):
        send_to_src(message, 'Wrong /setbudget command format!')
        return
    
    UserRepository.set_total_budget(
        db=db,
        telegram_id=user.telegram_id,
        total_budget_amount=user_data
    )
    send_to_src(message, 'Done.')

@bot.message_handler(commands=['remain'])
def remain_command(message: Message):
    user = get_user_from_message(m=message)

    send_to_src(message, str(UserRepository.budget_remain(db=db, telegram_id=user.telegram_id)))


    



bot.infinity_polling()