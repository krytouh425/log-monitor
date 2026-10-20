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