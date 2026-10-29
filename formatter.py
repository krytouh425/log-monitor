# Модуль форматирования — красиво выводим записи лога
# Используется для отображения в терминале и сохранения в файл

from datetime import datetime

# цвета для терминала (ANSI коды)
CVET_ERROR = "\033[91m"   # красный
CVET_WARN = "\033[93m"    # жёлтый
CVET_INFO = "\033[92m"    # зелёный
CVET_DEBUG = "\033[94m"   # синий
CVET_SBROS = "\033[0m"    # сброс цвета


class FormatterLoga:
    def __init__(self, tsvetnoj=True):
        self.tsvetnoj = tsvetnoj  # цветной вывод или нет

    def _cvet_urovnya(self, uroven):
        cvety = {
            "ERROR": CVET_ERROR,
            "WARN": CVET_WARN,
            "INFO": CVET_INFO,
            "DEBUG": CVET_DEBUG
        }
        return cvety.get(uroven, "")

    def formatirovat_zapis(self, zapis):
        # форматируем одну запись лога для вывода
        vremya = zapis.vremya.strftime("%H:%M:%S")
        istochnik = f"[{zapis.istochnik}] " if zapis.istochnik else ""

        if self.tsvetnoj:
            cvet = self._cvet_urovnya(zapis.uroven)
            return f"{vremya} {cvet}{zapis.uroven}{CVET_SBROS} {istochnik}{zapis.soobshenie}"

        return f"{vremya} {zapis.uroven} {istochnik}{zapis.soobshenie}"

    def formatirovat_vse(self, zapisi):
        return [self.formatirovat_zapis(z) for z in zapisi]

    def vyvesti(self, zapisi):
        for stroka in self.formatirovat_vse(zapisi):
            print(stroka)

    def v_fayl(self, zapisi, filepath):
        # сохраняем отформатированные записи в файл без цветов
        formatter_bez_tsveta = FormatterLoga(tsvetnoj=False)
        with open(filepath, "w", encoding="utf-8") as f:
            for stroka in formatter_bez_tsveta.formatirovat_vse(zapisi):
                f.write(stroka + "\n")
        print(f"✓ Записи сохранены: {filepath}")