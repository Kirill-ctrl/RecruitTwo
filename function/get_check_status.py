def check_status_applicant(status: str) -> bool:
    """Проверяем статус пользователя"""
    if status.lower() == 'applicant':
        return True
    else:
        return False
