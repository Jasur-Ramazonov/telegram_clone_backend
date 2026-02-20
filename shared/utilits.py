import re
phone_number_regex = r'^\+?[1-9]\d{7,14}$'
username_regex = r'^(?!.*__)[a-zA-Z][a-zA-Z0-9_]{2,30}[a-zA-Z0-9]$'
password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$'

def check_phone_number(phone_number:str)->bool:
    if re.fullmatch(phone_number_regex,phone_number):
        return True
    return False

def check_username(username:str)->bool:
    if re.fullmatch(username_regex,username):
        return True
    return False

def check_password(password:str)->bool:
    if re.fullmatch(password_regex,password):
        return True
    return False
