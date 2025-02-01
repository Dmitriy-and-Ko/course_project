from datetime import datetime
from pathlib import Path
from typing import Union
import pandas as pd
from pandas import DataFrame


PATH_TO_ROOT = Path(__file__).parent.parent
PATH_TO_DIR = Path(PATH_TO_ROOT, "data")


def time_of_day(my_date: str) -> str:
    """Функция принимает строку с датой и временем и возвращает строку с приветствием в текущем времени суток"""
    my_dt_obj = datetime.strptime(my_date, "%Y-%m-%d %H:%M:%S")
    time_obj = my_dt_obj.time()
    if time_obj < datetime.strptime("04:00:00", "%H:%M:%S").time():
        return "Доброй ночи"
    elif time_obj < datetime.strptime("11:00:00", "%H:%M:%S").time():
        return "Доброе утро"
    elif time_obj < datetime.strptime("16:00:00", "%H:%M:%S").time():
        return "Добрый день"
    else:
        return "Добрый вечер"


def read_excel(file_path: Union[str, Path]) -> DataFrame:
    """Функция принимает путь к excel файлу, читает и возвращает DataFrame объект"""
    df = pd.read_excel(file_path)
    return df


def reports_result(filename=None):
    """Внешняя функция, которая принимает аргумент filename для декоратора,
    для создания файла с результатами работы функции"""
    def inner(func):
        """Декоратор, принимает функцию для декорирования"""
        def wrapper(*args, **kwargs):
            """Функция обертка, которая принимает аргументы декорируемой функции"""
            res = func(*args, **kwargs)
            if filename:  # Проверка на наличие атрибута у filename
                path_to_file = Path(PATH_TO_DIR, filename)
                with open(path_to_file, "a", encoding="utf-8") as file:
                    file.write(f"Результат функции {func.__name__} =\n {res}\n")
            else:
                print(f"{func.__name__} отработала без записи в файл.\n")  # Выводим данные в консоль
            return res
        return wrapper
    return inner