from UsedClass.EmployerClass import Employer
from function.Information import get_status
import json
from function.Authentication import get_authorization
from function.response import not_authorized, access_denied
from function.get_check_status import check_status_applicant
from function.output import information_output


def convert_employer(list_tuple: list) -> list:
    """Преобразуем в список словарей"""
    list_dict = [{"name": list_tuple[i][0], "city": list_tuple[i][1]} for i in range(len(list_tuple))]
    return list_dict


def get_inf_employer(token: str, app) -> list or str:
    """Получаем список работодателей"""
    if get_authorization(token):
        status = get_status(token)
        if check_status_applicant(status):
            list_tuple = Employer().get_employer_list()
            data = convert_employer(list_tuple)
            return information_output(app, data)
        else:
            return access_denied()
    else:
        return not_authorized()
