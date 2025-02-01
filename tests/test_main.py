from src.main import main
from unittest.mock import patch
from src.utils import read_excel


def test_main():
    test_file_path = "C:/Users/USER/PycharmProjects/analysis_of_banking_operations/tests/test_operations.xlsx"
    test_date = "2021-12-10 10:44:39"
    with (patch('src.utils.read_excel', side_effect=lambda path: read_excel(path)
          if path == test_file_path else None),
          patch('builtins.input', side_effect=["1"]),
          patch('src.views.json_answer_web',
                return_value='{"greeting": "Доброе утро", '
                             '"cards": [{"last_digits": "*5091", "total_spent": 564.0, "cashback": 5.64}, '
                             '{"last_digits": "*7197", "total_spent": 78.05, "cashback": 0.7805}]}'),
          patch('src.services.categories_for_cashback'),
          patch('src.reports.spending_by_category')):
        result = main(test_file_path, test_date)
        assert result == ('{"greeting": "Доброе утро", '
                          '"cards": [{"last_digits": "*5091", "total_spent": 564.0, "cashback": 5.64}, '
                          '{"last_digits": "*7197", "total_spent": 78.05, "cashback": 0.7805}]}')


def test_main_services():
    # Путь к тестовому файлу
    test_file_path = "C:/Users/USER/PycharmProjects/analysis_of_banking_operations/tests/test_operations.xlsx"
    test_date = "2021-12-10 10:44:39"
    with (patch('src.utils.read_excel', side_effect=lambda path: read_excel(path)
          if path == test_file_path else None),
          patch('builtins.input', side_effect=["2"]),
          patch('src.views.json_answer_web'),
          patch('src.services.categories_for_cashback',
                return_value='{"Различные товары": 5.6, "Супермаркеты": 0.8}'),
          patch('src.reports.spending_by_category')):
        result = main(test_file_path, test_date)
        assert result == '{"Различные товары": 5.6, "Супермаркеты": 0.8}'


def test_main_reports():
    # Путь к тестовому файлу
    test_file_path = "C:/Users/USER/PycharmProjects/analysis_of_banking_operations/tests/test_operations.xlsx"
    test_date = "2021-12-10 10:44:39"
    with (patch('src.utils.read_excel', side_effect=lambda path: read_excel(path)
          if path == test_file_path else None),
          patch('builtins.input', side_effect=["3", "Супермаркеты", "31.12.2021"]),
          patch('src.views.json_answer_web'),
          patch('src.services.categories_for_cashback'),
          patch('src.reports.spending_by_category', return_value='{"Супермаркеты": 78.05}')):
        result = main(test_file_path, test_date)
        assert result == '{"Супермаркеты": 78.05}'