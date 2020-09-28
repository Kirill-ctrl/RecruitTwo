from UsedClass.ApplicantClass import Applicant
from UsedClass.QuestionClass import Question
from function.InformationApplicant import get_information_applicant
from UsedClass.AnswerClass import Answer1
from function.Information import get_status
from function.Authentication import get_authorization
from function.response import answers_already_added, not_authorized, access_denied, added
from function.get_check_status import check_status_applicant
from function.Connect import connecting
from function.response import answer_add_min_3, succesfully_answer_added, incorrect_id_qustion, answer_the_question_update
import json


def insert_answer_applicant(answer_applicant: list, question_id, token, code):
    """Добавляем ответы соискателя"""
    if get_authorization(token):
        status = get_status(token)
        if check_status_applicant(status):
            question = Question()
            cnt = question.get_count_question()
            question_id = int(question_id)
            if question_id <= cnt:
                applicant = Applicant()
                applicant_id = applicant.get_applicant_id(token)
                answer = Answer1()
                count = answer.check_answer_applicant(applicant_id)
                question = Question()
                count_question = question.count_question_by_code(code)
                if count >= count_question:
                    answer.update_answer(answer_applicant, question_id)
                    return answer_the_question_update()
                else:
                    applicant = Applicant()
                    applicant_id = applicant.get_applicant_id(token)
                    applicant.update_category_applicants(code, applicant_id)
                    answer.insert_answer_question(applicant_id, answer_applicant, question_id)
                    count = answer.count_answer_applicant(applicant_id)
                    if count < 3:
                        return answer_add_min_3()
                    else:
                        return succesfully_answer_added()
            else:
                return incorrect_id_qustion()
        else:
            return access_denied()
    else:
        return not_authorized()
