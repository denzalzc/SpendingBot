from termcolor import colored
from datetime import datetime, timezone
from telebot.types import Message
from re import match


# decors
def warn(text: str) -> None:
    print(colored(text, color='yellow'))
def good(text: str) -> None:
    print(colored(text, color='green'))
def bad(text: str) -> None:
    print(colored(text, color='red'))

# date
def now():
    return datetime.now(timezone.utc).replace(tzinfo=None)

# re
VALID_CATEGORIES = ["food", "transport", "entertainment", "utilities", "shopping", "health", "education", "other"]

def validate_category(category: str) -> bool:
    return True if category in [c for c in VALID_CATEGORIES] else False

def parse_user_message_addexpense(m: Message):
    pattern = r'^/add\s+(\d+(?:\.\d+)?)\s+(\w+)(?:\s+(.+))?$'
    shot = match(pattern=pattern, string=m.text)

    if shot:
        amount = shot.group(1)
        category = shot.group(2)

        if not(validate_category(category)):
            return 'categoryMistake'

        return {'amount': amount, 'category': category}
    else:
        return None
    
def parse_user_message_showexpense(m: Message):
    pattern = r'^/show(?:\s*(?:category\s+)?([a-zA-Z]+)?(?:\s+(\d+))?)?$'
    shot = match(pattern, m.text.strip())

    if shot:
        category = shot.group(1)
        count = shot.group(2)

        if not(category):
            return {'category': category, 'count': count} 
        
        if not(validate_category(category)):
            return 'categoryMistake'

        return {'category': category, 'count': count}
    else:
        return None

def parse_user_message_deleteexpense(m: Message):
    pattern = r'^/delete\s+(\d+)$'
    shot = match(pattern, m.text.strip())

    if shot:
        return int(shot.group(1))
    else:
        return False
    
def parse_user_message_totalexpense(m: Message):
    pattern = r'^/total(?:\s+(category\s+)?(\w+))?$'
    shot = match(pattern, m.text.strip())
    if not(shot):
        return False
    
    if not(shot.group(1)) and not(shot.group(2)):
        return [None, None]
    if not(shot.group(1)) and shot.group(2):
        if not(validate_category(shot.group(2))):
            return ['categoryMistake', shot.group(2)]
        return [shot.group(2), None]
    
def parse_user_message_updatebudget(m: Message):
    pattern = r'^/setbudget\s+(\d+(?:\.\d+)?)$'
    shot = match(pattern, m.text.strip())
    
    if shot:
        try:
            return float(shot.group(1))
        except ValueError:
            return None
    
    return None