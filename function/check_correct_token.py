from UsedClass.TokenClass import Token


def check_token(token):
    token_ekz = Token('None')
    value = token_ekz.check_token_correct(token)
    if value:
        return True
    else:
        return False
