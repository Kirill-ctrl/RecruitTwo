import psycopg2

DB_NAME = 'Recruit'
USER_NAME = 'postgres'
PASSWORD = 'k197908'


def connecting() -> tuple:
    """Пытаемся подключиться к БД"""
    with psycopg2.connect(f"dbname={DB_NAME} user={USER_NAME} password='{PASSWORD}'") as conn:
        cur = conn.cursor()
    return conn, cur
