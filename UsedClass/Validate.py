from marshmallow import Schema, fields, validate


class ValidateRegistration(Schema):
    """Валидируем регистрацию"""
    name = fields.String(required=True, error_messages={"required": "name is required"})
    email = fields.Email(required=True, error_messages={"required": "email is required", "invalid": "invalid email"})
    age = fields.Integer(required=True, error_messages={"required": "age is required"})
    city = fields.String(required=True, error_messages={"required": "city is required"})
    psw = fields.String(required=True, error_messages={"required": "psw is required"})
    repeat_psw = fields.String(required=True, error_messages={"required": "repeat_psw is required"})
    status = fields.String(required=True, error_messages={"required": "status is required"}, validate=validate.OneOf(["Applicant", "Employer"]))


class ValidateAuthorization(Schema):
    """Валидируем авторизацию"""
    email = fields.Email(required=True, error_messages={"required": "email is required", "invalid": "invalid email"})
    psw = fields.String(required=True, error_messages={"required": "psw is required"})


class ValidateAnswerApplicant(Schema):
    """Валидируем ответ пользователя"""
    answer = fields.String(required=True, error_messages={"required" : "answer is required"})
