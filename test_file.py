from function.ApplicantList import *
from UsedClass.AnswerClass import *
from function.EmployerList import *
from function.InformationApplicant import *
from function.InformationEmployer import *
from function.QuestionAll import *
from function.Registration import *
import requests
import json

token_employer = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRhcnlhQG1haWwucnUiLCJzdGF0dXMiOiJFbXBsb3llciJ9.VrxkDDbtEiVssoESaNxq_e5S4rtGQNrROsUeqcJt-6A'
token_applicant = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImtpcmlsbEBtYWlsLnJ1Iiwic3RhdHVzIjoiQXBwbGljYW50In0.EYkmQowOgZTs1n2KSvvoVunOtRMRT-VAe4RHoagbejk'
token_applicant2 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InNhc2hhQG1haWwucnUiLCJzdGF0dXMiOiJBcHBsaWNhbnQifQ.HeH0CbvFxLqj23_Zk6cG30VBVU7G7YwlPuuWu2IjSu0'


def test_applicant():
    payload = {'Token': token_employer}
    r = requests.get('http://127.0.0.1:5000/applicant', headers=payload)
    list_applicant = get_inf_applicant(payload['Token'])
    assert list_applicant == r.text


def test_get_authorisation():
    conn, cur = connecting()
    cur.execute(f"SELECT token_status FROM token WHERE token_text = '{token_employer}'")
    s = cur.fetchone()[0]
    assert isinstance(get_authorization(token_employer), bool)
    assert s == get_authorization(token_employer)


def test_get_status():
    conn, cur = connecting()
    cur.execute(f"SELECT status FROM users INNER JOIN token ON users.id = token.user_id WHERE token_text = '{token_employer}'")
    st = cur.fetchone()[0]
    status = get_status(token_employer)
    assert status == st
    assert isinstance(status, str)
    assert isinstance(st, str)


def test_list_applicant():
    job_seekers = Applicant()
    applic = Applicant()
    assert isinstance(job_seekers, Applicant)
    assert isinstance(applic, Applicant)
    conn, cur = connecting()
    cur.execute(f"SELECT * FROM applicant ORDER BY id")
    s = cur.fetchall()
    list_tuple = applic.get_applicant_list()
    assert s == list_tuple
    json_output = [
        {
            "id": 4,
            "name": "Kirill",
            "city": "Kazan",
            "age": 18,
            "email": "kirill@mail.ru",
            "question_list": 200,
            "employer_id": 6,
            "accept": True
        },
        {
            "id": 5,
            "name": "Sasha",
            "city": "Kazan",
            "age": 18,
            "email": "sasha@mail.ru",
            "question_list": None,
            "employer_id": None,
            "accept": False
        }
    ]
    assert convert_applicant(list_tuple) == json_output


def test_list_employer():
    payload = {'Token': token_applicant}
    r = requests.get('http://127.0.0.1:5000/employer', headers=payload)
    list_employer = get_inf_employer(payload['Token'])
    assert list_employer == r.text
    job_person = Employer()
    employ = Employer()
    assert isinstance(employ, Employer)
    assert isinstance(job_person, Employer)
    conn, cur = connecting()
    cur.execute(f"SELECT employer_name, city FROM employer ORDER BY id")
    s = cur.fetchall()
    list_tuple = employ.get_employer_list()
    assert s == list_tuple
    json_output = [
        {
            "name": "Darya",
            "city": "Perm"
        },
        {
            "name": "Danil",
            "city": "Kazan"
        }
    ]
    assert list_employer == r.text
    assert convert_employer(list_tuple) == json_output


def test_quest():
    z = get_questions(token_applicant)
    assert isinstance(json.loads(z), dict)
    ques = Question()
    random_id = ques.rand()
    assert isinstance(random_id, int)
    ques.give_random_id(random_id)
    quest = Question()
    assert isinstance(quest, Question)
    quest.give_random_id(random_id)
    s = quest.choice_quest()
    assert isinstance(s, list)
    f = quest.choice_code()
    assert isinstance(f, int)


def test_answer():
    code = 200
    payload = {'Token': token_applicant2, "code": f"{code}"}
    some_payload = {
        "1": "Знаю",
        "2": "Знаю",
        "3": "Знаю",
        "4": "Знаю"
    }
    assert isinstance(code, int)
    r = requests.post('http://127.0.0.1:5000/answer', headers=payload, json=some_payload)
    assert json.dumps('Добавлено') == r.text
    key_some_payload = []
    for key in some_payload:
        key_some_payload.append(some_payload[key])
    assert ["Знаю", "Знаю", "Знаю", "Знаю"] == key_some_payload
    name, email, status, users_id, applicant_id = get_information_applicant(token_applicant2)
    assert isinstance(name, str)
    assert isinstance(email, str)
    assert isinstance(status, str)
    assert isinstance(users_id, int)
    assert isinstance(applicant_id, int)
    quest = Question()
    list_quest_id = quest.id_quest(code)
    assert isinstance(list_quest_id, list)
    ans = Answer1()
    ans.give_applicant_id(applicant_id)
    list_answer = ans.check_answer()
    assert isinstance(list_answer, list)


def test_list():
    payload = {'Token': token_employer}
    r = requests.get('http://127.0.0.1:5000/list', headers=payload)
    json_output = [
        {
            "name": "Sasha",
            "city": "Kazan",
            "age": 18,
            "email": "sasha@mail.ru",
            "question_code": 200
        }
    ]
    assert r.text == json.dumps(json_output)


def test_answer_list():
    payload = {'Token': token_employer, "email": "kirill@mail.ru"}
    r = requests.get('http://127.0.0.1:5000/answer_list', headers=payload)
    json_output = [
        {
            "text_question": "Знания HTML",
            "text_answer": "Начальные"
        },
        {
            "text_question": "Знания CSS",
            "text_answer": "Нет"
        },
        {
            "text_question": "Знания JS",
            "text_answer": "Нет"
        },
        {
            "text_question": "Фремфорки JS и для чего они нужны?",
            "text_answer": "Не знаю"
        }
    ]
    assert r.text == json.dumps(json_output)


def test_accept():
    payload = {'Token': token_employer, "Employer-email": "darya@mail.ru", "Applicant-email": "kirill@mail.ru"}
    r = requests.get('http://127.0.0.1:5000/accept', headers=payload)
    assert json.dumps('Успешно обновлено') == r.text



