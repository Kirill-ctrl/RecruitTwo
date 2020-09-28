from UsedClass.UsersClass import Users
from function.Authentication import get_authorization
from function.response import successfully_exited, not_authorized


def log_out(token: str) -> str:
    """Выход из системы"""
    if get_authorization(token):
        user = Users()
        user.exit(token)
        return successfully_exited()
    else:
        return not_authorized()
