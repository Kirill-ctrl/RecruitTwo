import json
from UsedClass.QuestionClass import Question, QuestionList
from function.Information import get_status
from function.Authentication import get_authorization
from function.response import not_authorized, access_denied
from function.get_check_status import check_status_applicant
from function.output import information_output


def convert_dict(code: int, list_id_text_questions: list):
    """Преобразование в словарь"""
    beautiful_text_question = [{"Category": code}]
    for i in range(len(list_id_text_questions)):
        beautiful_text_question.append({
            "id": list_id_text_questions[i][0],
            "text_question": list_id_text_questions[i][1]
        })
    return beautiful_text_question


def get_questions(token: str, app) -> list or str:
    """Получаем случайные вопросы"""
    if get_authorization(token):
        status = get_status(token)
        if check_status_applicant(status):
            question = Question()
            question_list = QuestionList()
            random_id = question_list.rand()
            question.give_random_id(random_id)
            list_id_text_questions = question.choice_question()
            code = question_list.choice_code(random_id)
            data = convert_dict(code, list_id_text_questions)
            return information_output(app, data)
        else:
            return access_denied()
    else:
        return not_authorized()