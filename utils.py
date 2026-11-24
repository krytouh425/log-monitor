# Вспомогательные функции — общие утилиты для монитора логов
# Используются разными модулями приложения

import os
from datetime import datetime


def razmer_fayla_mb(filepath):
    # возвращаем размер файла в МБ
    if not os.path.exists(filepath):
        return 0
    return os.path.getsize(filepath) / (1024 * 1024)


def vozrast_fayla_dney(filepath):
    # сколько дней прошло с изменения файла
    if not os.path.exists(filepath):
        return 0
    vremya = os.path.getmtime(filepath)
    data = datetime.fromtimestamp(vremya)
    return (datetime.now() - data).days


def formatirovat_razmer(bayt):
    # форматируем размер в читаемый вид
    if bayt < 1024:
        return f"{bayt} Б"
    elif bayt < 1024 * 1024:
        return f"{bayt / 1024:.1f} КБ"
    else:
        return f"{bayt / (1024 * 1024):.1f} МБ"


def sozdat_papku(put):
    # создаём папку если её нет
    if not os.path.exists(put):
        os.makedirs(put)
        return True
    return False


def spisok_logov(papka="."):
    # возвращаем список лог-файлов в папке
    return [
        f for f in os.listdir(papka)
        if f.endswith(".log")
    ]


def tekushee_vremya():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")