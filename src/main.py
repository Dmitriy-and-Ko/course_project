from src.reports import spending_by_category
from src.services import categories_for_cashback
from src.utils import read_excel
from src.views import json_answer_web


def main(file_path: str, date) -> str:
    """Главная функция для получения JSON-ответов по категориям. Принимает путь к файлу и дату"""
    df = read_excel(file_path)
    print(
        """Введите категорию для получения JSON-ответа:
    1. Веб-страницы
    2. Сервисы
    3. Отчеты"""
    )
    while True:
        user_category = input("Введите целое число от 1 до 3: ")
        if user_category == "1":
            print("Ваша категория 'Веб-страницы'.")
            return json_answer_web(df, date)
        elif user_category == "2":
            print("Ваша категория 'Сервисы'.")
            return categories_for_cashback(df, date)
        elif user_category == "3":
            print("Ваша категория 'Отчеты'.")
            while True:
                user_category_payment = input("Введите категорию платежа: ")
                user_date_report = input("Введите дату для организации отчета(например: 10.10.2021): ")
                result = spending_by_category(df, user_category_payment, user_date_report)
                return result
