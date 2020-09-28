from function.Connect import connecting


def get_information_employer(token: str) -> tuple:
    """Получаем всю информацию о работодателе"""
    conn, cur = connecting()
    cur.execute(f"SELECT employer.employer_name, users.email, users.status, employer.users_id FROM users INNER JOIN token ON token.user_id = users.id INNER JOIN employer ON employer.users_id = "
                f"users.id WHERE token_text = '{token}'")
    s = cur.fetchall()
    name = s[0][0]
    email = s[0][1]
    status = s[0][2]
    user_id = s[0][3]
    return name, email, status, user_id
