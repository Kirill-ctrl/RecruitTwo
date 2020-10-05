from UsedClass.AnswerClass import Answer1
from UsedClass.ApplicantClass import Applicant
from function.Information import get_status
import function.Authentication
from function.response import access_denied, not_authorized, incorrect_token, page_is_not_found
from function.get_check_status import check_status_applicant
from function.output import information_output
from function.check_correct_token import check_token


def sort_ans_list(list_tuple) -> list:
    """Преобразует в словарь """
    list_dict = [{
        'id_question': list_tuple[i][0],
        'text_question': list_tuple[i][1],
        'text_answer': list_tuple[i][2]
    } for i in range(len(list_tuple))]
    return list_dict


def get_list_answer_applicant(token: str, email: str, app, pagination_result: str, pagination_after: str) -> list or str:
    """Получаем список ответов соискателя"""
    if check_token(token):
        if function.Authentication.get_authorization(token):
            status = get_status(token)
            if check_status_applicant(status):
                return access_denied()
            else:
                job_seeker = Applicant()
                name, email, status, users_id, applicant_id = job_seeker.get_information_from_email(email)
                job_seeker.give_applicant_id(applicant_id)

                ans = Answer1()
                ans.give_applicant_id(applicant_id)
                list_tuple = ans.get_answer_list(pagination_result, pagination_after)
                if list_tuple:

                    data = sort_ans_list(list_tuple)
                    return information_output(app, data)
                else:
                    return page_is_not_found()
        else:
            return not_authorized()
    else:
        return incorrect_token()
