import json
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd

PATH_TO_DIR = Path(__file__).parent.parent
PATH_TO_FILE_LOG = Path(PATH_TO_DIR, "logs", "services.log")

logger = logging.getLogger("services")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(PATH_TO_FILE_LOG, encoding="UTF-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def categories_for_cashback(my_data: pd.DataFrame, date: str) -> str:
    """Функция принимает DataFrame для анализа и дату, и анализирует
    сколько можно заработать кэшбека по каждой категории покупок в указанную дату"""
    date_time_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    month = date_time_obj.month
    year = date_time_obj.year
    my_data["Дата платежа"] = pd.to_datetime(my_data["Дата платежа"], format="%d.%m.%Y")

    logger.info("Преобразование столбца 'Дата платежа' в формат datetime выполнено успешно.")

    filtered_data_by_date = my_data[
        (my_data["Дата платежа"].dt.month == month) & (my_data["Дата платежа"].dt.year == year)
    ]
    expenses_data = filtered_data_by_date[filtered_data_by_date["Сумма операции"] < 0]
    cashback_by_category = expenses_data.groupby("Категория")["Сумма операции"].sum().abs()
    cashback_by_category = round((cashback_by_category / 100), 1).to_dict()

    logger.info("Словарь функции categories_for_cashback сформирован успешно.")

    json_for_services = json.dumps(cashback_by_category, ensure_ascii=False)
    return json_for_services
