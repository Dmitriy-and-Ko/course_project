import os
from unittest.mock import patch

from src.views import get_cards_group_by_expenses, get_currency_rate, get_price_of_stock


def test_get_cards_group_by_expenses(data_views_expenses):
    expected_result = [
        {"last_digits": "*1234", "total_spent": 150, "cashback": 1.5},  # 150 = 100 + 50
        {"last_digits": "*5678", "total_spent": 500, "cashback": 5.0},  # 200 = 200
        {"last_digits": "*9101", "total_spent": 150, "cashback": 1.5},  # 150 = 150
    ]
    result = get_cards_group_by_expenses(data_views_expenses)
    assert result == expected_result


@patch("requests.get")
def test_get_price_of_stock_AAPL(mock_get):
    mock_get.return_value.text = '{"stock": "AAPL", "price": "1"}'
    assert get_price_of_stock("AAPL") == "1"
    stock_name = "AAPL"
    STOCK_API_KEY = os.getenv("STOCK_API-KEY")
    mock_get.assert_called_once_with(f"https://api.twelvedata.com/price?symbol={stock_name}&apikey={STOCK_API_KEY}")


@patch("requests.get")
def test_get_price_of_stock_AMZN(mock_get_stock):
    mock_get_stock.return_value.text = '{"stock": "AMZN", "price": "1"}'
    assert get_price_of_stock("AMZN") == "1"
    stock_name = "AMZN"
    STOCK_API_KEY = os.getenv("STOCK_API-KEY")
    mock_get_stock.assert_called_once_with(
        f"https://api.twelvedata.com/price?symbol={stock_name}&apikey={STOCK_API_KEY}"
    )


@patch("requests.get")
def test_get_price_of_stock_GOOGL(mock_get_GOOGL):
    mock_get_GOOGL.return_value.text = '{"stock": "GOOGL", "price": "1"}'
    assert get_price_of_stock("GOOGL") == "1"
    stock_name = "GOOGL"
    STOCK_API_KEY = os.getenv("STOCK_API-KEY")
    mock_get_GOOGL.assert_called_once_with(
        f"https://api.twelvedata.com/price?symbol={stock_name}&apikey={STOCK_API_KEY}"
    )


@patch("requests.get")
def test_get_price_of_stock_MSFT(mock_get_MSFT):
    mock_get_MSFT.return_value.text = '{"stock": "MSFT", "price": "1"}'
    assert get_price_of_stock("MSFT") == "1"
    stock_name = "MSFT"
    STOCK_API_KEY = os.getenv("STOCK_API-KEY")
    mock_get_MSFT.assert_called_once_with(
        f"https://api.twelvedata.com/price?symbol={stock_name}&apikey={STOCK_API_KEY}"
    )


@patch("requests.get")
def test_get_price_of_stock_TSLA(mock_get_TSLA):
    mock_get_TSLA.return_value.text = '{"stock": "TSLA", "price": "1"}'
    assert get_price_of_stock("TSLA") == "1"
    stock_name = "TSLA"
    STOCK_API_KEY = os.getenv("STOCK_API-KEY")
    mock_get_TSLA.assert_called_once_with(
        f"https://api.twelvedata.com/price?symbol={stock_name}&apikey={STOCK_API_KEY}"
    )


@patch("requests.request")
def test_get_currency_USD(mock_get_USD):
    mock_get_USD.return_value.text = '{"query": {"from": "USD", "to": "RUB", "amount": 1}, "result": 102.469555}'
    assert get_currency_rate("USD") == 102.469555
    current_string = "USD"
    CURRENCY_API_KEY = os.getenv("CURRENCY_API-KEY")
    payload = {}
    headers = {"apikey": CURRENCY_API_KEY}
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={current_string}&amount=1"
    mock_get_USD.assert_called_once_with("GET", url, headers=headers, data=payload)


@patch("requests.request")
def test_get_currency_EUR(mock_get_EUR):
    mock_get_EUR.return_value.text = '{"query": {"from": "EUR", "to": "RUB", "amount": 1}, "result": 121.15}'
    assert get_currency_rate("EUR") == 121.15
    current_string = "EUR"
    CURRENCY_API_KEY = os.getenv("CURRENCY_API-KEY")
    payload = {}
    headers = {"apikey": CURRENCY_API_KEY}
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={current_string}&amount=1"
    mock_get_EUR.assert_called_once_with("GET", url, headers=headers, data=payload)
