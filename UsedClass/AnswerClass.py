from DBClass.DataBaseClass import AnswerTable


class Answer1:

    def __init__(self):
        self.db = AnswerTable()
        self.code = None
        self.list_quest_id = None
        self.key_answer_dict = None
        self.applicant_id = None
        self.list_id_questions = None

    def give_data_answer(self, code: int, key_answer_dict: list, list_id_questions: list) -> None:
        """Получаем информацию о пользователе"""
        self.code = code
        self.list_id_questions = list_id_questions
        self.key_answer_dict = key_answer_dict

    def give_applicant_id(self, applicant_id: int) -> None:
        """Получаем id соискателя 1 """
        self.applicant_id = applicant_id

    def get_answer_list(self) -> list:
        """Получаем ответы (текст ответа и id вопросов) соискателя 1 """
        list_tuple = self.db.get_answer_list_applicants(self.applicant_id)
        return list_tuple

    def check_answer_applicant(self, applicant_id: int) -> int:
        """"""
        count = self.db.check_answer_the_question(applicant_id)
        return count

    def check_cnt_question(self, question_id: int):
        cont = self.db.check_count_the_question_category(question_id)
        return cont

    def update_answer(self, answer_applicant, question_id: int) -> None:
        """"""
        self.db.update_answer_the_question(answer_applicant, question_id)

    def insert_answer_question(self, applicant_id: int, answer_applicant, question_id: int) -> None:
        """"""
        self.db.insert_answer_the_question_applicant(applicant_id, answer_applicant, question_id)

    def count_answer_applicant(self, applicant_id: int) -> int:
        """"""
        count = self.db.get_count_answer_applicant(applicant_id)
        return count
