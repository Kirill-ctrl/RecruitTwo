from DBClass.DataBaseClass import UsersTable


class Users:
    def __init__(self):
        self.db = UsersTable()
        self.name = None
        self.email = None
        self.password = None
        self.status = None
        self.status = None

    def add_new_user(self, name: str, email: str, password: str, status: str) -> None:
        """Получаем информацию по пользователю 1 """
        self.name = name
        self.email = email
        self.password = password
        self.status = status
        self.db.adding_new_user(name, email, password, status)

    def get_id_user(self) -> int:
        """Получаем id нового пользователя 1 """
        users_id = self.db.get_id_new_user(self.email)
        return users_id

    def get_id_users(self, email: str) -> int:
        """Получаем id пользователя 1  2"""
        user_id = self.db.get_id_user(email)
        return user_id

    def get_psw(self, email: str) -> str:
        """Получаем пароль пользователя по email"""
        password = self.db.get_password(email)
        return password

    def get_status(self, email: str) -> str:
        """Получаем статус пользователя по email 1 """
        status = self.db.get_status_users(email)
        return status

    def get_email(self, token: str) -> str:
        """Получаем email пользователя по token 1 """
        email = self.db.get_email_user_by_token(token)
        return email

    def exit(self, token: str) -> None:
        """Выходим из системы 1 """
        self.db.log_out(token)


class PictureUsers:

    def __init__(self):
        self.db = UsersTable()

    def add_photo(self, path, user_id):
        answer = self.db.added_photo_user(path, user_id)
        return answer

    def get_path_picture(self, token):
        path = self.db.get_path_picture_by_token(token)
        return path