from DBClass.DataBaseClass import EmployerTable


class Employer:

    def __init__(self):
        self.db = EmployerTable()
        self.name = None
        self.email = None
        self.token = None
        self.status = None
        self.user_id = None

    def get_information_employer(self, name: str, email: str, token: str, status: str, user_id: int) -> None:
        """Получаем информацию по работодателю"""
        self.name = name
        self.email = email
        self.token = token
        self.status = status
        self.user_id = user_id

    def get_employer_list(self) -> list:
        """Получаем список работодателей 1 """
        list_tuple = self.db.employer_list()
        return list_tuple

    def add_new_employer(self, name: str, city: str, users_id: int) -> None:
        """Добавляем нового работодателя"""
        self.db.new_employer(name, city, users_id)

    def get_employer_id(self, employer_email: str) -> int:
        """Получаем id работодателя по email 1 """
        return self.db.get_id_by_email(employer_email)
