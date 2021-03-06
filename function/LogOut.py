from UsedClass.UsersClass import Users
import function.Authentication
from function.response import successfully_exited, not_authorized, incorrect_token
from function.check_correct_token import check_token


def log_out(token: str) -> str:
    """Выход из системы"""
    if check_token(token):
        if function.Authentication.get_authorization(token):
            user = Users()
            user.exit(token)
            return successfully_exited()
        else:
            return not_authorized()
    else:
        return incorrect_token()
