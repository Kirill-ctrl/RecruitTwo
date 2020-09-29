from DBClass.DataBaseClass import TokenTable


class Token:

    def __init__(self, email: str):
        self.db = TokenTable()
        self.token = None
        self.user_id = None
        self.email = email

    def insert_token(self, token: str, user_id: int, time_now) -> None:
        """Добавляем токен 1 """
        self.db.insert_token(token, user_id, time_now)

    def count_authorization(self) -> int:
        """Считаем количество авторизаций пользователя 1"""
        count = self.db.amount_of_authorizations(self.email)
        return count

    def insert_new_token_temp(self, new_token_temp: str, user_id: int, time_now, new_date) -> None:
        """Добавляем новый временный токен 1"""
        self.db.insert_new_temporary_token(new_token_temp, user_id, time_now, new_date, self.email)

    def get_status_and_id(self) -> tuple:
        """Получаем статус и id пользователя 1"""
        list_tuples = self.db.get_status_and_user_id_by_email(self.email)
        user_id = 0
        for i in range(len(list_tuples)):
            user_id = list_tuples[i][1] + 1
        status = list_tuples[0][0]
        return user_id, status

    def update_status_token(self, time_now) -> None:
        """Обновляем статус токена при входе в систему 1 2"""
        self.db.update_token_status(time_now, self.email)

    def single_token(self) -> str:
        """Получаем единственный токен соискателя 1 """
        token = self.db.get_single_token(self.email)
        return token

    def get_save_temp(self) -> list:
        """Получаем время сохранения временных токенов 1 """
        save_temp = self.db.get_save_time(self.email)
        return save_temp

    def get_bool_token_status(self, token: str) -> bool:
        """Получаем токен статус для авторизации 1 """
        bool_value = self.db.get_bool_value_token_status(token)
        return bool_value

    def delete_token(self, list_save_temp) -> None:
        """Удаляем просроченные токены 1 """
        self.db.remove_expired_tokens(list_save_temp)

    def check_token_correct(self, token):
        token = self.db.check_correct_token_users(token)
        return token
