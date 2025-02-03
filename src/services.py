import json
from datetime import datetime

import pandas as pd


def categories_for_cashback(my_data: pd.DataFrame, date: str) -> str:
    """Функция принимает DataFrame для анализа и дату, и анализирует
    сколько можно заработать кэшбека по каждой категории покупок в указанную дату"""
    date_time_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    month = date_time_obj.month
    year = date_time_obj.year
    my_data["Дата платежа"] = pd.to_datetime(my_data["Дата платежа"], format="%d.%m.%Y")
    filtered_data_by_date = my_data[
        (my_data["Дата платежа"].dt.month == month) & (my_data["Дата платежа"].dt.year == year)
    ]
    expenses_data = filtered_data_by_date[filtered_data_by_date["Сумма операции"] < 0]
    cashback_by_category = expenses_data.groupby("Категория")["Сумма операции"].sum().abs()
    cashback_by_category = round((cashback_by_category / 100), 1).to_dict()
    json_for_services = json.dumps(cashback_by_category, ensure_ascii=False)
    return json_for_services
