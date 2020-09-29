from function.Connect import connecting
from function.check_correct_token import check_token
from function.response import incorrect_token


def get_information_employer(token: str) -> tuple:
    """Получаем всю информацию о работодателе"""
    if check_token(token):
        conn, cur = connecting()
        cur.execute(f"SELECT employer.employer_name, users.email, users.status, employer.users_id FROM users INNER JOIN token ON token.user_id = users.id INNER JOIN employer ON employer.users_id = "
                    f"users.id WHERE token_text = '{token}'")
        s = cur.fetchall()
        name = s[0][0]
        email = s[0][1]
        status = s[0][2]
        user_id = s[0][3]
        return name, email, status, user_id
    else:
        return incorrect_token()