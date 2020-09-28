from UsedClass.ApplicantClass import Applicant
from function.Information import get_status
from function.Authentication import get_authorization
from UsedClass.EmployerClass import Employer
from function.response import not_authorized, access_denied, successfully_updated
from function.get_check_status import check_status_applicant


def accept_applicant(token: str, employer_email: str, applicant_email: str) -> str:
    """Принимаем соискателя на работу"""
    if get_authorization(token):
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
