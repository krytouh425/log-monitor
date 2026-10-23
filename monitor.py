# Модель записи лога — основная единица данных монитора
# Каждая строка лог-файла превращается в объект LogZapis

from datetime import datetime


# уровни логирования которые мы обрабатываем
UROVNI = ("ERROR", "WARN", "INFO", "DEBUG")


class LogZapis:
    def __init__(self, vremya, uroven, soobshenie, istochnik=None):
        self.vremya = vremya        # datetime объект
        self.uroven = uroven        # ERROR / WARN / INFO / DEBUG
        self.soobshenie = soobshenie
        self.istochnik = istochnik  # имя сервиса или модуля

    def to_dict(self):
        return {
            "vremya": self.vremya.strftime("%Y-%m-%d %H:%M:%S"),
            "uroven": self.uroven,
            "soobshenie": self.soobshenie,
            "istochnik": self.istochnik
        }

    def __repr__(self):
        ист = f"[{self.istochnik}]" if self.istochnik else ""
        return f"{self.vremya.strftime('%H:%M:%S')} {self.uroven} {ист} {self.soobshenie}"

# Модуль чтения лога — парсит лог-файл построчно
# Поддерживает стандартный формат: ГГГГ-ММ-ДД ЧЧ:ММ:СС УРОВЕНЬ [источник] сообщение

import re
import os

FAYL_LOGA = "server.log"  # лог-файл сервера по умолчанию

# шаблон строки лога
SHABLON = re.compile(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"  # дата и время
    r"(ERROR|WARN|INFO|DEBUG)\s+"                   # уровень
    r"(?:\[(.+?)\]\s+)?"                            # источник (опционально)
    r"(.+)"                                         # сообщение
)


class ChitateLoga:
    def __init__(self, filepath=FAYL_LOGA):
        self.filepath = filepath

    def proverit_fayl(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Лог-файл не найден: {self.filepath}")
        if os.path.getsize(self.filepath) == 0:
            raise ValueError("Лог-файл пустой")

    def razobrat_stroku(self, stroka, nomer):
        # пробуем распарсить строку по шаблону
        stroka = stroka.strip()
        if not stroka:
            return None

        sovpadenie = SHABLON.match(stroka)
        if not sovpadenie:
            print(f"! Строка {nomer}: не соответствует формату, пропускаем")
            return None

        vremya_str, uroven, istochnik, soobshenie = sovpadenie.groups()

        try:
            vremya = datetime.strptime(vremya_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print(f"! Строка {nomer}: неверный формат времени, пропускаем")
            return None

        return LogZapis(vremya, uroven, soobshenie.strip(), istochnik)

    def zagruzit(self):
        self.proverit_fayl()
        zapisi = []

        with open(self.filepath, encoding="utf-8") as f:
            for nomer, stroka in enumerate(f, start=1):
                zapis = self.razobrat_stroku(stroka, nomer)
                if zapis:
                    zapisi.append(zapis)

        print(f"Загружено записей: {len(zapisi)}")
        return zapisi