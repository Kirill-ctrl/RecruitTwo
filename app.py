from flask import Flask, request
from function.ApplicantList import get_inf_applicant, get_applicant_list_for_employer
from function.EmployerList import get_inf_employer
from function.QuestionAll import get_questions
from function.AnswerAll import insert_answer_applicant
from function.AnswerListApplicant import get_list_answer_applicant
from function.AcceptOnWork import accept_applicant
from function.Registration import sign_up
from function.Authentication import auth
from function.LogOut import log_out
from UsedClass.Validate import ValidateRegistration, ValidateAuthorization, ValidateAnswerApplicant
from marshmallow import ValidationError
import pickle
from PIL import Image
from struct import *
from ctypes import *
import os
from Connect import connecting
from UsedClass.UsersClass import Users
from function.picture import photo

app = Flask(__name__)


@app.route('/applicant')
def applicant():
    token = request.headers['Token']
    pagination_result = request.args.get('pagination_result')
    pagination_after = request.args.get('pagination_after')
    return get_inf_applicant(token, app, pagination_result, pagination_after)


@app.route('/employer')
def employer():
    token = request.headers['Token']
    pagination_result = request.args.get('pagination_result')
    pagination_after = request.args.get('pagination_after')
    return get_inf_employer(token, app, pagination_result, pagination_after)


@app.route('/quest')
def quest():
    token = request.headers['Token']
    pagination_result = request.args.get('pagination_result')
    pagination_after = request.args.get('pagination_after')
    return get_questions(token, app, pagination_result, pagination_after)


@app.route('/answer/<question_id>', methods=['POST'])
def answer(question_id: int):
    dict_answer_applicant = request.json
    answer_applicant = dict_answer_applicant["answer"]
    token = request.headers['Token']
    code = request.headers['code']
    try:
        result = ValidateAnswerApplicant().load(dict_answer_applicant)
        code = request.headers['code']
        token = request.headers['Token']
        return insert_answer_applicant(answer_applicant, question_id, token, code)
    except ValidationError as err:
        return err.messages


@app.route("/list")
def get_list():
    token = request.headers['Token']
    pagination_result = request.args.get('pagination_result')
    pagination_after = request.args.get('pagination_after')
    return get_applicant_list_for_employer(token, app, pagination_result, pagination_after)


@app.route('/answer_list')
def answer_list():
    token = request.headers['Token']
    email = request.headers['Email']
    pagination_result = request.args.get('pagination_result')
    pagination_after = request.args.get('pagination_after')
    return get_list_answer_applicant(token, email, app, pagination_result, pagination_after)


@app.route('/accept')
def accept():
    token = request.headers['Token']
    employer_email = request.headers['Employer-email']
    applicant_email = request.headers['Applicant-email']
    return accept_applicant(token, employer_email, applicant_email)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        result = ValidateRegistration().load(data)
        return sign_up(data)
    except ValidationError as err:
        return err.messages


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    try:
        result = ValidateAuthorization().load(data)
        return auth(data)
    except ValidationError as err:
        return err.messages


@app.route('/logout')
def logout():
    token = request.headers['Token']
    return log_out(token)


@app.route('/index', methods=['POST'])
def index():
    file = request.get_data('capture')
    name = request.headers['filename']
    token = request.headers['Token']

    return photo(file, name, token)


def find(name):
    for root, dirs, files in os.walk('/'):
        if name in files:
            return os.path.join(root, name)


if __name__ == '__main__':
    app.run()
