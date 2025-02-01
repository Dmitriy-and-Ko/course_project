import pandas as pd
import json
from src.reports import spending_by_category


def test_spending_by_category(data):
    transactions = pd.DataFrame(data)
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")
    category = "Супермаркеты"
    date = "25.01.2021"  # Тестируем на дату, которая входит в диапазон
    expected_result = json.dumps({"Супермаркеты": 350}, ensure_ascii=False)
    result = spending_by_category(transactions, category, date)
    assert result == expected_result


def test_spending_by_category_with_none_date(data):
    transactions = pd.DataFrame(data)
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")
    category = "Супермаркеты"
    expected_result = json.dumps({}, ensure_ascii=False, indent=4)
    result = spending_by_category(transactions, category, None)
    assert result == expected_result