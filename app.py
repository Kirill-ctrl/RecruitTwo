from flask import Flask, request, send_file
from flask_mail import Mail
import function.ApplicantList
import function.EmployerList
from function.QuestionAll import get_questions
from function.AnswerAll import insert_answer_applicant
from function.AnswerListApplicant import get_list_answer_applicant
from function.AcceptOnWork import accept_applicant
import function.Registration
import function.Authentication
from function.LogOut import log_out
from UsedClass.Validate import ValidateRegistration, ValidateAuthorization, ValidateAnswerApplicant
from marshmallow import ValidationError
from function.picture import photo, get_picture
from config import Config_Mail


app = Flask(__name__)

app.config.from_object(Config_Mail)

mail = Mail(app)


@app.route('/applicant')
def applicant():
    token = request.headers.get('Token')
    pagination_result = request.args.get('pagination_result')
    pagination_after = request.args.get('pagination_after')
    return function.ApplicantList.get_inf_applicant(token, app, pagination_result, pagination_after)


@app.route('/employer')
def employer():
    token = request.headers.get('Token')
    pagination_result = request.args.get('pagination_result')
    pagination_after = request.args.get('pagination_after')
    return function.EmployerList.get_inf_employer(token, app, pagination_result, pagination_after)


@app.route('/quest')
def quest():
    token = request.headers.get('Token')
    pagination_result = request.args.get('pagination_result')
    pagination_after = request.args.get('pagination_after')
    return get_questions(token, app, pagination_result, pagination_after)


@app.route('/answer/<question_id>', methods=['POST'])
def answer(question_id: int):
    dict_answer_applicant = request.json
    answer_applicant = dict_answer_applicant.get("answer")
    try:
        result = ValidateAnswerApplicant().load(dict_answer_applicant)
        code = request.headers.get('code')
        token = request.headers.get('Token')
        return insert_answer_applicant(answer_applicant, question_id, token, code)
    except ValidationError as err:
        return err.messages


@app.route("/list")
def get_list():
    token = request.headers.get('Token')
    pagination_result = request.args.get('pagination_result')
    pagination_after = request.args.get('pagination_after')
    return function.ApplicantList.get_applicant_list_for_employer(token, app, pagination_result, pagination_after)


@app.route('/answer_list')
def answer_list():
    token = request.headers.get('Token')
    email = request.headers.get('Email')
    pagination_result = request.args.get('pagination_result')
    pagination_after = request.args.get('pagination_after')
    return get_list_answer_applicant(token, email, app, pagination_result, pagination_after)


@app.route('/accept')
def accept():
    token = request.headers.get('Token')
    employer_email = request.headers.get('Employer-email')
    applicant_email = request.headers.get('Applicant-email')
    return accept_applicant(token, employer_email, applicant_email)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        result = ValidateRegistration().load(data)
        return function.Registration.sign_up(data)
    except ValidationError as err:
        return err.messages


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    try:
        result = ValidateAuthorization().load(data)
        return function.Authentication.auth(data)
    except ValidationError as err:
        return err.messages


@app.route('/logout')
def logout():
    token = request.headers.get('Token')
    return log_out(token)


@app.route('/save_photo', methods=['POST'])
def save_photo():
    file = request.files.get('capture')
    token = request.headers.get('Token')
    return photo(file, token)


@app.route('/photo')
def get_photo():
    token = request.headers.get('Token')
    try:
        path, mimetype = get_picture(token)
        return send_file(path, mimetype=mimetype)
    except:
        return get_picture(token)


@app.route('/confirmation', methods=["POST"])
def conf():
    get_code = request.form.get("code")
    token = request.headers.get("Token")
    return function.Registration.confirmation(get_code, token)


if __name__ == '__main__':
    app.run()
