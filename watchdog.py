# Модуль watchdog — следим за появлением новых записей в логе
# Используется для мониторинга в реальном времени на проде

import os
import time
from datetime import datetime


class WatchdogLoga:
    def __init__(self, filepath, interval=5):
        self.filepath = filepath
        self.interval = interval  # секунд между проверками
        self.poslednyaya_pozitsiya = 0
        self.schetchik_oshibok = 0

    def _proverit_fayl(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Лог-файл не найден: {self.filepath}")

    def _chitat_novye_stroki(self):
        # читаем только новые строки с последней проверки
        novye = []
        with open(self.filepath, encoding="utf-8") as f:
            f.seek(self.poslednyaya_pozitsiya)
            for stroka in f:
                novye.append(stroka.strip())
            self.poslednyaya_pozitsiya = f.tell()
        return [s for s in novye if s]

    def _obrabotit_stroku(self, stroka):
        # проверяем строку на наличие ошибок
        if "ERROR" in stroka:
            self.schetchik_oshibok += 1
            print(f"🔴 [{datetime.now().strftime('%H:%M:%S')}] ОШИБКА: {stroka}")
        elif "WARN" in stroka:
            print(f"🟡 [{datetime.now().strftime('%H:%M:%S')}] WARN: {stroka}")

    def zapustit(self, max_iteratsiy=None):
        self._proverit_fayl()
        iteratsiy = 0
        print(f"Watchdog запущен — слежу за {self.filepath}")
        print("Для остановки нажмите Ctrl+C\n")

        try:
            while True:
                novye = self._chitat_novye_stroki()
                for stroka in novye:
                    self._obrabotit_stroku(stroka)

                iteratsiy += 1
                if max_iteratsiy and iteratsiy >= max_iteratsiy:
                    break

                time.sleep(self.interval)

        except KeyboardInterrupt:
            print(f"\nWatchdog остановлен")
            print(f"Обнаружено ошибок за сессию: {self.schetchik_oshibok}")