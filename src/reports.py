import json
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from pathlib import Path
import logging


PATH_TO_DIR = Path(__file__).parent.parent
PATH_TO_FILE_LOG = Path(PATH_TO_DIR, "logs", "reports.log")

logger = logging.getLogger("reports")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(PATH_TO_FILE_LOG, encoding="UTF-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None):
    """Функция принимает датафрэйм, категорию покупки и дату
    и возвращает все покупки по данной категории за последние три месяца"""
    try:
        if date is None:
            date = datetime.now().strftime("%d.%m.%Y")

            logger.info("Дата не была передана в функцию spending_by_category.")

        end_date = datetime.strptime(date, "%d.%m.%Y")
        start_date = end_date - timedelta(days=90)
    except Exception as ex:
        logger.error(f"Произошла ошибка {ex}")
        return ex

    logger.info(f"Успешно определены временные промежутки в функции spending_by_category.")

    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")
    filtered_transactions = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата платежа"] >= start_date)
        & (transactions["Дата платежа"] <= end_date)
    ]
    res = filtered_transactions.groupby("Категория")["Сумма платежа"].sum().abs()
    res_dict = res.to_dict()

    logger.info(f"Сформирован словарь функции spending_by_category.")

    json_answer = json.dumps(res_dict, ensure_ascii=False)
    return json_answer

