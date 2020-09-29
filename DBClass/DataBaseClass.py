import psycopg2


class DataBase:
    DB_NAME = 'Recruit'
    USER_NAME = 'postgres'
    PASSWORD = 'k197908'

    def __init__(self):
        self.conn, self.cur = self.connecting()

    def connecting(self) -> tuple:
        """Подключаемся к БД"""
        with psycopg2.connect(f"dbname={self.DB_NAME} user={self.USER_NAME} password='{self.PASSWORD}'") as conn:
            cur = conn.cursor()
        return conn, cur


class ApplicantTable(DataBase):

    def applicant_list(self, pagination_result: str, pagination_after: str) -> list:
        """Запрашивает всю информацию соискателей из БД"""
        self.cur.execute(f"SELECT * FROM applicant ORDER BY id OFFSET {int(pagination_after)} LIMIT {int(pagination_result)}")
        list_tuple = self.cur.fetchall()
        return list_tuple

    def applicant_list_for_employers(self, pagination_result, pagination_after) -> list:
        """Получает информацию о соискателях для запроса /list"""
        self.cur.execute(f"SELECT applicant_name, city, age, email, question_list_code FROM applicant WHERE accept = false ORDER BY id OFFSET {int(pagination_after)} LIMIT {int(pagination_result)}")
        list_tuples = self.cur.fetchall()
        return list_tuples

    def update_applicant_accepted(self, employer_id: int, applicant_email: str) -> None:
        """Ставит соискателю id работодателя, который принял его на работу"""
        self.cur.execute(f"UPDATE applicant SET employer_id = {employer_id}, accept = true WHERE email = '{applicant_email}'")
        self.conn.commit()

    def get_data_by_email(self, email: str) -> list:
        """Выбирает информацию о соискатлях по email"""
        self.cur.execute(f"SELECT applicant.applicant_name, users.email, users.status, applicant.users_id, applicant.id FROM users INNER JOIN applicant ON "
                         f"applicant.users_id = users.id WHERE users.email = '{email}'")
        list_tuple = self.cur.fetchall()
        return list_tuple

    def new_applicant(self, name: str, city: str, age: int, email: str, users_id: int) -> None:
        """Добавляет нового соискателя"""
        self.cur.execute(f"INSERT INTO applicant(applicant_name, city, age, email, users_id) VALUES ('{name}', '{city}', {age}, '{email}', {int(users_id)})")
        self.conn.commit()

    def get_applicant_id_by_token(self, token: str) -> int:
        """Получаем id по email"""
        self.cur.execute(f"SELECT applicant.id FROM applicant INNER JOIN token ON token.user_id = applicant.users_id WHERE token_text = '{token}'")
        applicant_id = self.cur.fetchone()[0]
        return applicant_id

    def update_category_question_applicant(self, code: int, applicant_id: int) -> None:
        """Ставит соискателю код вопросов, на которые он ответил"""
        self.cur.execute(f"UPDATE applicant SET question_list_code = {code} WHERE id = {applicant_id}")
        self.conn.commit()


class EmployerTable(DataBase):

    def employer_list(self, pagination_result: str, pagination_after: str) -> list:
        """Выбирает всю информацию о работодателях"""
        self.cur.execute(f"SELECT employer_name, city FROM employer ORDER BY id OFFSET {int(pagination_after)} LIMIT {int(pagination_result)}")
        list_tuple = self.cur.fetchall()
        return list_tuple

    def new_employer(self, name: str, city: str, users_id: int) -> None:
        """Добавляет нового работодателя"""
        self.cur.execute(f"INSERT INTO employer(employer_name, city, users_id) VALUES ('{name}', '{city}', {int(users_id)})")
        self.conn.commit()

    def get_id_by_email(self, employer_email: str) -> int:
        """Получает id работодателя по email"""
        self.cur.execute(f"SELECT employer.id FROM employer INNER JOIN users ON users.id = employer.users_id WHERE email = '{employer_email}'")
        employer_id = self.cur.fetchone()[0]
        return employer_id


class TokenTable(DataBase):

    def insert_token(self, token: str, user_id: int, time_now) -> None:
        """Добавляет токен"""
        self.cur.execute(f"""INSERT INTO token(token_text, user_id, token_time) VALUES ('{token}', {int(user_id)}, '{time_now}')""")
        self.conn.commit()

    def amount_of_authorizations(self, email: str) -> int:
        """Считает количество авторизаций"""
        self.cur.execute(f"SELECT COUNT(token.id) FROM token INNER JOIN users ON token.user_id = users.id WHERE email = '{email}' AND token_status = true")
        count = self.cur.fetchone()[0]
        return count

    def insert_new_temporary_token(self, new_token_temp: str, user_id: int, time_now, new_date, email: str) -> None:
        """Добавляет новый временный токен"""
        self.cur.execute(f"""INSERT INTO token(token_text, user_id, token_time, save_temp, token_status) VALUES ('{new_token_temp}', {int(user_id)}, '{time_now}', '{new_date}', {True})""")
        self.conn.commit()

    def get_status_and_user_id_by_email(self, email: str) -> list:
        """ВЫбирает статус и id юзера по email"""
        self.cur.execute(f"SELECT status, token.id FROM users INNER JOIN token ON token.user_id = users.id WHERE email = '{email}' ORDER BY token.id")
        list_tuples = self.cur.fetchall()
        return list_tuples

    def update_token_status(self, time_now, email: str) -> None:
        """Обновляет токен статус при входе в систему"""
        self.cur.execute(f"UPDATE token SET token_status = True, token_time = '{time_now}' WHERE user_id = (SELECT id FROM users WHERE email = '{email}') AND token_status = false")
        self.conn.commit()

    def get_single_token(self, email: str) -> str:
        """Возвращает токен, если он первый и не активирован"""
        self.cur.execute(f"SELECT token_text FROM token INNER JOIN users ON users.id = token.user_id WHERE email = '{email}'")
        token = self.cur.fetchone()[0]
        return token

    def get_save_time(self, email: str) -> list:
        """Получает время, на которые нужно было сохранить временные токены"""
        self.cur.execute(f"SELECT save_temp FROM token INNER JOIN users ON token.user_id = users.id WHERE email = '{email}'")
        save_temp = self.cur.fetchall()
        return save_temp

    def get_bool_value_token_status(self, token: str) -> bool:
        """Получает токен статус для проверки авторизации"""
        self.cur.execute(f"SELECT token_status FROM token WHERE token_text = '{token}'")
        bool_value = self.cur.fetchone()[0]
        return bool_value

    def remove_expired_tokens(self, list_save_temp: list) -> None:
        """Удаляет временные токены, если их срок действия истек"""
        for i in range(len(list_save_temp)):
            if list_save_temp:
                self.cur.execute(f"DELETE FROM token WHERE save_temp = '{list_save_temp[i]}'")
                self.conn.commit()


class AnswerTable(DataBase):

    def get_answer_list_applicants(self, applicant_id: int, pagination_result, pagination_after) -> list:
        """Выбирает id вопросов, текст ответов для /answer_list"""
        self.cur.execute(
            f"SELECT id_quest, quest_text, text_answer FROM answer INNER JOIN question ON id = id_quest WHERE user_id = {applicant_id} OFFSET {int(pagination_after)} LIMIT {int(pagination_result)}")
        list_tuple = self.cur.fetchall()
        return list_tuple

    def check_answer_the_question(self, applicant_id: int, code):
        """Проверяет сколько вопросов всего есть в этой категории"""
        self.cur.execute(f"SELECT COUNT(user_id) FROM answer INNER JOIN question ON question.id = answer.id_quest INNER JOIN question_list ON question.question_list_id = question_list.id  "
                         f"WHERE user_id = {applicant_id} AND question_list.code = {code}")
        count_answer = self.cur.fetchone()[0]
        return count_answer

    def check_count_the_question_category(self, question_id: int) -> int:
        """Проверяет сколько вопросов всего есть в этой категории"""
        self.cur.execute(f"SELECT COUNT(id_quest) FROM question WHERE id_quest = {question_id}")
        cont = self.cur.fetchone()[0]
        return cont

    def update_answer_the_question(self, answer_applicant: str, question_id: int) -> None:
        """Обновляет ответ на вопрос"""
        self.cur.execute(f"UPDATE answer SET text_answer = '{answer_applicant}' WHERE id_quest = {question_id}")
        self.conn.commit()

    def insert_answer_the_question_applicant(self, applicant_id: int, answer_applicant: str, question_id: int) -> None:
        """Добавляем ответы соискателя в таблицу"""
        self.cur.execute(f"INSERT INTO answer(user_id, text_answer, id_quest) VALUES ({applicant_id}, '{answer_applicant}', {question_id})")
        self.conn.commit()

    def get_count_answer_applicant(self, applicant_id: int) -> int:
        """Проверяет сколько вопросов добавлено от соискателя"""
        self.cur.execute(f"SELECT COUNT(user_id) FROM answer WHERE user_id = {applicant_id}")
        count = self.cur.fetchone()[0]
        return count


class UsersTable(DataBase):

    def adding_new_user(self, name: str, email: str, password: str, status: str) -> None:
        """Добавляет нового пользователя в таблицу users"""
        self.cur.execute(f"INSERT INTO users(name, email, psw, status) VALUES ('{name}', '{email}', '{password}', '{status}')")
        self.conn.commit()

    def get_id_new_user(self, email: str) -> int:
        """Выбирает id нового пользователя по email"""
        self.cur.execute(f"SELECT id FROM users WHERE email = '{email}'")
        users_id = self.cur.fetchone()[0]
        return users_id

    def get_id_user(self, email: str) -> int:
        """Выбирает id пользователя по email"""
        self.cur.execute(f"SELECT id FROM users WHERE email = '{email}'")
        user_id = self.cur.fetchone()[0]
        return user_id

    def get_password(self, email: str) -> str:
        """Выбирает пароль пользователя по email"""
        self.cur.execute(f"SELECT psw FROM users WHERE email = '{email}'")
        list_tuple = self.cur.fetchone()
        return list_tuple[0]

    def get_status_users(self, email: str) -> str:
        """Выбирает статус пользователя по email"""
        self.cur.execute(f"SELECT status FROM users INNER JOIN token ON token.user_id = users.id WHERE email = '{email}' ORDER BY token.id")
        status = self.cur.fetchone()[0]
        return status

    def get_email_user_by_token(self, token: str) -> str:
        """Выбирает email пользователя по token"""
        self.cur.execute(f"SELECT email FROM users INNER JOIN token ON users.id = user_id WHERE token_text = '{token}'")
        email = self.cur.fetchone()[0]
        return email

    def log_out(self, token: str) -> None:
        """Обновляет статус токена в false при выходе из системы"""
        self.cur.execute(f"UPDATE token SET token_status = False WHERE token_text = '{token}'")
        self.conn.commit()

    def added_photo_user(self, path, user_id):
        self.cur.execute(f"INSERT INTO UserPicture(path, users_id) VALUES ('{path}', {user_id})")
        self.conn.commit()


class QuestionTable(DataBase):

    def get_text_questions(self, random_id: int, pagination_result, pagination_after) -> list:
        """Выбирает текст вопросов и псевдонимы по random_id"""
        self.cur.execute(f"SELECT id, quest_text FROM question WHERE question_list_id = {random_id} ORDER BY id OFFSET {int(pagination_after)} LIMIT {int(pagination_result)}")
        list_tuples = self.cur.fetchall()
        return list_tuples

    def get_question_text_by_id_question(self, id_questions: list) -> list:
        """Выбирает текст вопроса по id вопроса, важен порядок"""
        self.cur.execute(f"SELECT id, quest_text FROM question WHERE id IN {id_questions}")
        list_tuple = self.cur.fetchall()
        return list_tuple

    def get_all_count_question(self) -> int:
        """Общее количество существующих вопросов"""
        self.cur.execute(f"SELECT COUNT(id) FROM question")
        cnt = self.cur.fetchone()[0]
        return cnt

    def get_count_question_by_code(self, code: int) -> int:
        self.cur.execute(f"SELECT COUNT(question.id) FROM question INNER JOIN question_list ON question.question_list_id = question_list.id WHERE code = {code}")
        cnt_question = self.cur.fetchone()[0]
        return cnt_question


class QuestionListTable(DataBase):

    def get_list_id(self) -> list:
        """Выбирает id категории вопросов"""
        self.cur.execute("SELECT id FROM question_list ")
        list_tuples = self.cur.fetchall()
        return list_tuples

    def select_question_code(self, random_id: int) -> list:
        """Выбирает code категории вопросов"""
        self.cur.execute(f"SELECT code FROM question_list WHERE id = {random_id}")
        list_tuple = self.cur.fetchone()
        return list_tuple


class CodeApplicantTable(DataBase):

    def add_code_in_code_applicant(self, code, applicant_id):
        self.cur.execute(f"INSERT INTO CodeApplicants(code, applicant_id) VALUES ({code}, {applicant_id})")
        self.conn.commit()

    def check_answer_code_in_CodeApplicant(self, applicant_id):
        self.cur.execute(f"SELECT code FROM CodeApplicants WHERE applicant_id = {applicant_id}")
        code = self.cur.fetchall()
        return code
