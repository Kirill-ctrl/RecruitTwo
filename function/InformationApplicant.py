from function.Connect import connecting


def get_information_applicant(token: str) -> tuple:
    """Получаем всю информацию о соискателе"""
    conn, cur = connecting()
    cur.execute(f"SELECT applicant.applicant_name, users.email, users.status, applicant.users_id, applicant.id FROM users INNER JOIN token ON token.user_id = users.id INNER JOIN applicant ON "
                f"applicant.users_id = "
                f"users.id WHERE token_text = '{token}'")
    list_tuple = cur.fetchall()
    name = list_tuple[0][0]
    email = list_tuple[0][1]
    status = list_tuple[0][2]
    users_id = list_tuple[0][3]
    applicant_id = list_tuple[0][4]
    return name, email, status, users_id, applicant_id
