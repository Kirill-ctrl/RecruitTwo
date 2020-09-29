import json
from flask import jsonify
from flask import make_response


def answer_must_more_than_3() -> str:
    response = make_response(jsonify({"code": 411, "text_response": "Min Count Length Required answer: 3"}), 406)
    return response


def access_denied() -> str:
    """"""
    response = make_response(jsonify({"code": 403, "text_response": "Forbidden"}), 406)
    return response


def not_authorized() -> str:
    """"""
    response = make_response(jsonify({"code": 401, "text_response": "Unauthorized"}), 406)
    return response


def answers_already_added() -> str:
    response = make_response(jsonify({"code": 208, "text_response": "Already Reported"}), 406)
    return response


def added() -> str:
    response = make_response(jsonify({"Code": 201, "text_response": "Created"}), 406)
    return response


def successfully_updated() -> str:
    """"""
    response = make_response(jsonify({"Code": 202, "text_response": "Accepted"}), 406)
    return response


def incorrect_filling() -> str:
    response = make_response(jsonify({"Code": 406, "text_response": "Not Acceptable"}), 406)
    return response


def email_already_exists() -> str:
    response = make_response(jsonify({"Code": 208, "text_response": "Already Reported"}), 208)
    return response


def data_added_save_token(token: str) -> str:
    response = make_response(jsonify({"Code": 200, "text_response": "OK", "Token": token}), 200)
    return response


def try_again() -> str:
    response = make_response(jsonify({"Code": 426, "text_response": "Upgrade Required", "add information": "check data"}), 426)
    return response


def token_verification_successful() -> str:
    response = make_response(jsonify({"Code": 200, "text_response": "OK"}), 200)
    return response


def successfully_logged_get_token(token: str) -> str:
    response = make_response(jsonify({"Code": 200, "text_response": "OK", "Token": token}), 200)
    return response


def more_than_3_entered() -> str:
    response = make_response(jsonify({"Code": 406, "text_response": "Not Acceptable", "additional parameter needed": "Token-time , Count(days)"}), 406)
    return response


def successfully_exited() -> str:
    response = make_response(jsonify({"Code": 200, "text_response": "OK"}), 200)
    return response


def answer_add_min_3():
    """"""
    response = make_response(jsonify({"Code": 202, "text_response": "Accepted", "Min-Length-answer": 3}), 202)
    return response


def succesfully_answer_added():
    """"""
    response = make_response(jsonify({"Code": 202, "text_response": "Accepted"}), 202)
    return response


def incorrect_id_qustion():
    """"""
    response = make_response(jsonify({"Code": 404, "text_response": "Not Found", "additional_information": "incorrect id"}), 404)
    return response


def answer_the_question_update():
    """"""
    response = make_response(jsonify({"Code": 202, "text_response": "Accepted"}), 202)
    return response


def check_correct_please():
    response = make_response(jsonify({"Code": 406, "text_response": "Not Acceptable", "additional parameter needed": "Token-time , Count(days)"}), 406)
    return response


def incorrect_date():
    response = make_response(jsonify({"Code": 404, "text_response": "Not Found", "additional_information": "incorrect_date"}), 404)
    return response


def mistake_create_token():
    response = make_response(jsonify({"Code": 500, "text_response": "Internal Server Error", "additional_information": "Token creation error"}), 500)
    return response


def incorrect_token():
    response = make_response({"code": 404, "text_response": "Incorrect Token"})
    return response


def incorrect_mimetype():
    response = make_response({"code": 404, "text_response": "Incorrect Mimetype"})
    return response

def page_is_not_found():
    response = make_response({"code": 404, "text_response": "Page is not found"})
    return response