import json

import pandas as pd

from src.services import categories_for_cashback


def test_categories_for_cashback():
    data = {
        "Дата платежа": ["01.01.2021", "15.01.2021", "20.01.2021", "25.01.2021"],
        "Сумма операции": [-100, -200, -300, -400],
        "Категория": ["Еда", "Транспорт", "Еда", "Развлечения"],
    }
    my_data = pd.DataFrame(data)
    expected_result = {"Еда": 4.0, "Развлечения": 4.0, "Транспорт": 2.0}
    result = categories_for_cashback(my_data, "2021-01-20 00:00:00")
    result_dict = json.loads(result)
    assert result_dict == expected_result
