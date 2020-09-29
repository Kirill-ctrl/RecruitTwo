from random import choices
from DBClass.DataBaseClass import QuestionTable, QuestionListTable


class Question:

    def __init__(self):
        self.db = QuestionTable()
        self.random_id = None

    def give_random_id(self, random_id: int):
        """"""
        self.random_id = random_id

    def choice_question(self, pagination_result, pagination_after) -> list:
        """выбрать вопросы по определенному id 1 """
        list_tuples = self.db.get_text_questions(self.random_id, pagination_result, pagination_after)
        return list_tuples

    def get_quest_text(self, id_questions: list) -> tuple:
        """"""
        list_tuple = self.db.get_question_text_by_id_question(id_questions)
        text_question = [list_tuple[i][1] for i in range(len(list_tuple))]
        id_text_question = [list_tuple[i][0] for i in range(len(list_tuple))]
        return text_question, id_text_question

    def get_count_question(self) -> int:
        """"""
        cnt = self.db.get_all_count_question()
        return cnt

    def count_question_by_code(self, code: int) -> int:
        cnt_question = self.db.get_count_question_by_code(code)
        return cnt_question


class QuestionList:

    def __init__(self):
        self.db = QuestionListTable()
        self.random_id = None
        self.code = None

    def rand(self) -> int:
        """Выбор случайного id категории вопросов 1 """
        list_tuples = self.db.get_list_id()
        list_random = []
        for i in range(len(list_tuples)):
            list_random.append(list_tuples[i][0])
        list_random = choices(list_random, k=1)
        self.random_id = list_random[0]
        return list_random[0]

    def choice_code(self, random_id: int) -> int:
        """Выбрать код вопросов по random_id 1 """
        list_tuple = self.db.select_question_code(random_id)
        self.code = list_tuple[0]
        return list_tuple[0]
