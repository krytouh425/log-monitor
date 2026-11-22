# Модуль парсинга — разбираем строки лога по шаблону
# Поддерживает несколько форматов логов

import re
from datetime import datetime

# стандартный формат: 2026-11-22 09:15:00 ERROR [service] сообщение
SHABLON_STANDART = re.compile(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"(ERROR|WARN|INFO|DEBUG)\s+"
    r"(?:\[(.+?)\]\s+)?"
    r"(.+)"
)

# короткий формат: 09:15:00 ERROR сообщение
SHABLON_KOROTKIY = re.compile(
    r"(\d{2}:\d{2}:\d{2})\s+"
    r"(ERROR|WARN|INFO|DEBUG)\s+"
    r"(.+)"
)


class ParserStroki:
    def __init__(self, data_loga=None):
        # дата лога нужна для короткого формата
        self.data_loga = data_loga or datetime.now().strftime("%Y-%m-%d")

    def razobrat(self, stroka):
        stroka = stroka.strip()
        if not stroka:
            return None

        # пробуем стандартный формат
        sovpadenie = SHABLON_STANDART.match(stroka)
        if sovpadenie:
            vremya_str, uroven, istochnik, soobshenie = sovpadenie.groups()
            try:
                vremya = datetime.strptime(vremya_str, "%Y-%m-%d %H:%M:%S")
                return {
                    "vremya": vremya,
                    "uroven": uroven,
                    "istochnik": istochnik,
                    "soobshenie": soobshenie.strip()
                }
            except ValueError:
                pass

        # пробуем короткий формат
        sovpadenie = SHABLON_KOROTKIY.match(stroka)
        if sovpadenie:
            vremya_str, uroven, soobshenie = sovpadenie.groups()
            try:
                vremya = datetime.strptime(
                    f"{self.data_loga} {vremya_str}",
                    "%Y-%m-%d %H:%M:%S"
                )
                return {
                    "vremya": vremya,
                    "uroven": uroven,
                    "istochnik": None,
                    "soobshenie": soobshenie.strip()
                }
            except ValueError:
                pass

        return None

    def razobrat_vse(self, stroki):
        rezultaty = []
        neparsennye = 0

        for stroka in stroki:
            rezultat = self.razobrat(stroka)
            if rezultat:
                rezultaty.append(rezultat)
            elif stroka.strip():
                neparsennye += 1

        if neparsennye:
            print(f"! Не удалось разобрать строк: {neparsennye}")

        return rezultaty