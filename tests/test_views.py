import json
from unittest.mock import patch
from src.views import json_answer_web, get_cards_group_by_expenses


def test_json_answer_web(data_views):
    test_date = "2021-01-01 12:20:00"
    expected_result = {
        "greeting": "Добрый день",
        "cards": {
            "*1234": 100,
            "*5678": 200
        }
    }
    with patch('src.utils.time_of_day', return_value="Добрый день"), \
            patch('src.views.get_cards_group_by_expenses', return_value=expected_result["cards"]):
        result = json_answer_web(data_views, test_date)
        result_dict = json.loads(result)
        assert result_dict == expected_result


def test_get_cards_group_by_expenses(data_views_expenses):
    expected_result = [
        {"last_digits": "*1234", "total_spent": 150, "cashback": 1.5},  # 150 = 100 + 50
        {"last_digits": "*5678", "total_spent": 500, "cashback": 5.0},  # 200 = 200
        {"last_digits": "*9101", "total_spent": 150, "cashback": 1.5}  # 150 = 150
    ]
    result = get_cards_group_by_expenses(data_views_expenses)
    assert result == expected_result