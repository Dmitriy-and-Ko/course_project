from src.main import main
from unittest.mock import patch
from src.utils import read_excel
from pathlib import Path

PATH_TO_DIR = Path(__file__).parent.parent
PATH_TO_FILE = Path(PATH_TO_DIR, 'data', 'operations.xlsx')


def test_main():
    test_file_path = "C:/Users/user/OneDrive/Desktop/my-prj/course_project/data/operations.xlsx"
    test_date = "2021-12-10 10:44:39"
    with (patch('src.utils.read_excel', side_effect=lambda path: read_excel(path)
        if path == test_file_path else None),
        patch('builtins.input', side_effect=["1"]),
        patch('src.views.json_answer_web',
            return_value='{"greeting": "Доброе утро", "cards": [{"last_digits": "*1112", "total_spent": 46207.08, "cashback": 462.0708}, {"last_digits": "*4556", "total_spent": 1768837.24, "cashback": 17688.3724}, {"last_digits": "*5091", "total_spent": 17367.5, "cashback": 173.675}, {"last_digits": "*5441", "total_spent": 470854.8, "cashback": 4708.548}, {"last_digits": "*5507", "total_spent": 84000.0, "cashback": 840.0}, {"last_digits": "*6002", "total_spent": 69200.0, "cashback": 692.0}, {"last_digits": "*7197", "total_spent": 2389912.73, "cashback": 23899.1273}]}'),
        patch('src.services.categories_for_cashback'),
        patch('src.reports.spending_by_category')):
        result = main(test_file_path, test_date)
        assert result == ('{"greeting": "Доброе утро", "cards": [{"last_digits": "*1112", "total_spent": 46207.08, "cashback": 462.0708}, {"last_digits": "*4556", "total_spent": 1768837.24, "cashback": 17688.3724}, {"last_digits": "*5091", "total_spent": 17367.5, "cashback": 173.675}, {"last_digits": "*5441", "total_spent": 470854.8, "cashback": 4708.548}, {"last_digits": "*5507", "total_spent": 84000.0, "cashback": 840.0}, {"last_digits": "*6002", "total_spent": 69200.0, "cashback": 692.0}, {"last_digits": "*7197", "total_spent": 2389912.73, "cashback": 23899.1273}]}')


def test_main_services():
    # Путь к тестовому файлу
    test_file_path = "C:/Users/user/OneDrive/Desktop/my-prj/course_project/data/operations.xlsx"
    test_date = "2021-12-10 10:44:39"
    with (patch('src.utils.read_excel', side_effect=lambda path: read_excel(path)
        if path == test_file_path else None),
        patch('builtins.input', side_effect=["2"]),
        patch('src.views.json_answer_web'),
        patch('src.services.categories_for_cashback',
            return_value='{"Аптеки": 14.1, "Госуслуги": 1.8, "Детские товары": 0.3, "Дом и ремонт": 60.8, "Другое": 0.2, "Ж/д билеты": 36.6, "ЖКХ": 142.2, "Канцтовары": 7.1, "Каршеринг": 93.7, "Косметика": 0.2, "Местный транспорт": 21.6, "НКО": 0.1, "Одежда и обувь": 5.2, "Переводы": 699.9, "Развлечения": 34.0, "Различные товары": 13.8, "Связь": 3.4, "Сервис": 1.0, "Супермаркеты": 56.7, "Такси": 4.5, "Топливо": 2.2, "Транспорт": 1.2, "Услуги банка": 7.3, "Фастфуд": 39.9, "Цветы": 6.0, "Электроника и техника": 35.0}'),
        patch('src.reports.spending_by_category')):
        result = main(test_file_path, test_date)
        assert result == '{"Аптеки": 14.1, "Госуслуги": 1.8, "Детские товары": 0.3, "Дом и ремонт": 60.8, "Другое": 0.2, "Ж/д билеты": 36.6, "ЖКХ": 142.2, "Канцтовары": 7.1, "Каршеринг": 93.7, "Косметика": 0.2, "Местный транспорт": 21.6, "НКО": 0.1, "Одежда и обувь": 5.2, "Переводы": 699.9, "Развлечения": 34.0, "Различные товары": 13.8, "Связь": 3.4, "Сервис": 1.0, "Супермаркеты": 56.7, "Такси": 4.5, "Топливо": 2.2, "Транспорт": 1.2, "Услуги банка": 7.3, "Фастфуд": 39.9, "Цветы": 6.0, "Электроника и техника": 35.0}'


def test_main_reports():
    # Путь к тестовому файлу
    test_file_path = "C:/Users/user/OneDrive/Desktop/my-prj/course_project/data/operations.xlsx"
    test_date = "2021-12-10 10:44:39"
    with (patch('src.utils.read_excel', side_effect=lambda path: read_excel(path)
        if path == test_file_path else None),
        patch('builtins.input', side_effect=["3", "Супермаркеты", "31.12.2021"]),
        patch('src.views.json_answer_web'),
        patch('src.services.categories_for_cashback'),
        patch('src.reports.spending_by_category', return_value='{"Супермаркеты": 25931.62}')):
        result = main(test_file_path, test_date)
        assert result == '{"Супермаркеты": 25931.62}'