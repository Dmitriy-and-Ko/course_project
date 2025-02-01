import json
from typing import Any
import pandas as pd
from src.utils import time_of_day


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
        "cards": get_cards_group_by_expenses(data)
    }
    result = json.dumps(my_dict, ensure_ascii=False)
    return result