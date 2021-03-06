from UsedClass.ApplicantClass import Applicant
from function.Information import get_status
import function.Authentication
from UsedClass.EmployerClass import Employer
from function.response import not_authorized, access_denied, successfully_updated, incorrect_token
from function.get_check_status import check_status_applicant
from function.check_correct_token import check_token


def accept_applicant(token: str, employer_email: str, applicant_email: str) -> str:
    """Принимаем соискателя на работу"""
    if check_token(token):
        if function.Authentication.get_authorization(token):
            status = get_status(token)
            if check_status_applicant(status):
                return access_denied()
            else:
                employ = Employer()
                employer_id = employ.get_employer_id(employer_email)
                job_seeker = Applicant()
                job_seeker.accept_applicant(employer_id, applicant_email)
                return successfully_updated()
        else:
            return not_authorized()
    else:
        return incorrect_token()
