import json
import logging
import os
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

from src.utils import time_of_day

PATH_TO_DIR = Path(__file__).parent.parent
PATH_TO_ENV = Path(PATH_TO_DIR, ".env")
PATH_TO_JSON = Path(PATH_TO_DIR, "user_settings.json")

load_dotenv(PATH_TO_ENV)
STOCK_API_KEY = os.getenv("STOCK_API-KEY")
CURRENCY_API_KEY = os.getenv("CURRENCY_API-KEY")

PATH_TO_FILE_LOG = Path(PATH_TO_DIR, "logs", "views.log")

logger = logging.getLogger("views")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(PATH_TO_FILE_LOG, encoding="UTF-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_price_of_stock(stock_name: str) -> str:
    """Функция принимает на вход название одной из 5 акций: AAPL, AMZN, GOOGL, MSFT, TSLA и возвращает её
    действительную цену"""
    response = requests.get(f"https://api.twelvedata.com/price?symbol={stock_name}&apikey={STOCK_API_KEY}")
    try:
        json_str = response.text
        dict_result = json.loads(json_str)
        price_stock = dict_result.get("price")

        logger.info(f"Получена цена акции {stock_name} = {price_stock}")

        return price_stock
    except requests.RequestException as ex:
        return f"Произошла ошибка {ex}"


def get_currency_rate(current_string: str) -> float:
    """Функция принимает на вход название валюты в виде USD или EUR и возвращает её курс по отношению к рублю"""
    try:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={current_string}&amount=1"

        "apikey: YOUR API KEY"

        payload = {}
        headers = {"apikey": CURRENCY_API_KEY}

        response = requests.request("GET", url, headers=headers, data=payload)
        result = response.text
        dict_result = json.loads(result)
        currency_price = dict_result.get("result")

        logger.info(f"Получен курс {current_string} = {currency_price} руб.")

        return currency_price
    except requests.RequestException as ex:
        return f"Произошла ошибка {ex}"


def get_data_for_json_about_currency(path_json: str) -> dict:
    """Функция принимает на вход путь к файлу JSON с указанными валютами, по которым необходимо узнать курс.
    Ответ выдаёт в виде словаря."""
    with open(PATH_TO_JSON, "r", encoding="utf-8") as file_json:
        json_dict = json.load(file_json)
    list_currencies = json_dict.get("user_currencies")
    list_of_currencies_price = []
    for element in list_currencies:
        currency_price = get_currency_rate(element)
        list_of_currencies_price.append({"currency": element, "rate": currency_price})

        logger.info(f"Сформирован курс валют для out_json.json файла по шаблону {path_json}")

    return list_of_currencies_price


def get_data_for_json_about_stocks(path_json: str) -> dict:
    """Функция принимает на вход путь к файлу JSON с указанными акциями, по которым необходимо узнать
    цену. Ответ выдаёт в виде словаря."""
    with open(PATH_TO_JSON, "r", encoding="utf-8") as file_json:
        json_dict = json.load(file_json)
    list_stocks = json_dict.get("user_stocks")
    list_of_stocks_price = []
    for element in list_stocks:
        stock_price = get_price_of_stock(element)
        list_of_stocks_price.append({"stock": element, "price": stock_price})

        logger.info(f"Сформирован список цен акций для out_json.json файла по шаблону {path_json}")

    return list_of_stocks_price


def get_cards_group_by_expenses(df_transaction: pd.DataFrame) -> list[dict[str, float | Any]]:
    """Функция принимает dataframe с тарнзакциями и возвращает сгруппированный и отфильтрованный словарь
    с маской номера карты, суммой расходов и кэшбеком по сумме расходов"""
    filtered_df = df_transaction.loc[df_transaction["Сумма операции"] < 0]
    cards_df = filtered_df.groupby(["Номер карты"])  # Группируем по номеру карты
    new_df = cards_df["Сумма операции"].sum()  # Суммируем операции
    result_list = []
    # Добавляем кэшбек и формируем список
    for card_number, total in new_df.items():
        result_list.append(
            {"last_digits": card_number, "total_spent": abs(total), "cashback": abs(total / 100)}  # 1 руб. на 100 руб.
        )
    return result_list


def json_answer_web(data: pd.DataFrame, date: str):
    my_dict = {
        "greeting": time_of_day(date),
        "cards": get_cards_group_by_expenses(data),
        "currency_rates": get_data_for_json_about_currency(PATH_TO_JSON),
        "stock_prices": get_data_for_json_about_stocks(PATH_TO_JSON),
    }
    result = json.dumps(my_dict, ensure_ascii=False)
    return result


