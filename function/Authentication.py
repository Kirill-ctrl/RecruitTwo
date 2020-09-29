from werkzeug.security import check_password_hash
import jwt
from flask import request, make_response
from function.Registration import save_tkn
from datetime import *
from UsedClass.UsersClass import Users
from UsedClass.TokenClass import Token
from function.response import try_again, token_verification_successful, incorrect_token, more_than_3_entered, successfully_logged_get_token, check_correct_please, mistake_create_token, incorrect_date
from function.check_correct_token import check_token


def auth(data: dict) -> str:
    """Авторизация пользователя"""
    email = data['email']
    psw = data['psw']
    user = Users()
    passw = user.get_psw(email)
    password = check_password_hash(passw, psw)
    if password:
        token_users = Token(email)
        count = token_users.count_authorization()
        if count >= 3:
            check_save_token_temp(email)
            return get_token_temp(count, email)
        elif count == 0:
            return first_token_authorization(email)
        else:
            return get_new_token(email)
    else:
        return try_again()


def check_save_token_temp(email: str) -> str:
    """Проверяем временные токены"""
    token_user = Token(email)
    save_temp = token_user.get_save_temp()
    list_save_temp = []
    for i in range(len(save_temp)):
        if save_temp[i][0]:
            d = date.today()
            if save_temp[i][0] - d < timedelta(days=0):
                list_save_temp.append(save_temp[i][0])
    token_user.delete_token(list_save_temp)
    return token_verification_successful()


def get_token_temp(count: int, email: str) -> str:
    """Получаем временный токен"""
    try:
        user = Users()
        status = user.get_status(email)
        token_time = request.headers['Token-time']
    except:
        return check_correct_please()
    try:
        time_now = datetime.now()
        time_temp = timedelta(days=int(token_time))
        new_date = time_now + time_temp
        r = new_date.isoformat(timespec='hours')
        new_date = r[0:10]
    except:
        return incorrect_date()
    try:
        new_token_temp = jwt.encode({'email': email, 'token_time': token_time, 'i': count + 1, 'status': status}, 'secret', algorithm='HS256')
        response = make_response()
        response.headers['Token'] = new_token_temp
        new_token_temp = response.headers['Token']
        del response.headers['Token']
    except:
        return mistake_create_token()
    try:
        user_id = user.get_id_users(email)
        new_token = Token(email)
        new_token.insert_new_token_temp(new_token_temp, user_id, time_now, new_date)
        return successfully_logged_get_token(new_token_temp)
    except:
        return more_than_3_entered()


def get_new_token(email: str) -> str:
    """Получаем новый не временный токен"""
    token = Token(email)
    user_id, status = token.get_status_and_id()
    new_token = jwt.encode({'email': email, 'status': status, 'id': user_id}, 'secret', algorithm='HS256')
    response = make_response()
    response.headers['Token'] = new_token
    new_token = response.headers['Token']
    del response.headers['Token']
    save_tkn(new_token, email)
    time_now = datetime.now()
    token.update_status_token(time_now)
    return successfully_logged_get_token(new_token)


def first_token_authorization(email: str) -> str:
    """Получаем токен при первой авторизации"""
    new_token = Token(email)
    token = new_token.single_token()
    time_now = datetime.now()
    new_token.update_status_token(time_now)
    return successfully_logged_get_token(token)


def get_authorization(token: str) -> bool:
    """Получаем токен статус для проверки авторизации пользователя"""
    if check_token(token):
        user = Users()
        email = user.get_email(token)
        token_user = Token(email)
        bool_value = token_user.get_bool_token_status(token)
        return bool_value
    else:
        return incorrect_token()
