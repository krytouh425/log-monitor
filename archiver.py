# Модуль архивирования логов — сжимаем старые файлы для экономии места
# Запускается по расписанию или вручную дежурным администратором

import os
import gzip
import shutil
from datetime import datetime, timedelta

ARCHIVE_DIR = "archive"     # папка для архивов
STARYE_POSLE_DNEY = 7       # архивируем файлы старше 7 дней


class ArkhivatorLogov:
    def __init__(self, log_dir=".", archive_dir=ARCHIVE_DIR):
        self.log_dir = log_dir
        self.archive_dir = archive_dir
        self._sozdat_papku()

    def _sozdat_papku(self):
        if not os.path.exists(self.archive_dir):
            os.makedirs(self.archive_dir)

    def _vozrast_fayla(self, filepath):
        # считаем возраст файла в днях
        vremya_izmeneniya = os.path.getmtime(filepath)
        data = datetime.fromtimestamp(vremya_izmeneniya)
        return (datetime.now() - data).days

    def _szhať_fayl(self, filepath):
        # сжимаем файл в gzip и перемещаем в архив
        imya = os.path.basename(filepath)
        archive_path = os.path.join(self.archive_dir, imya + ".gz")

        with open(filepath, "rb") as f_in:
            with gzip.open(archive_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        os.remove(filepath)
        return archive_path

    def arhivirovat_starye(self):
        # находим и архивируем старые лог-файлы
        arhivirovano = []

        for fayl in os.listdir(self.log_dir):
            if not fayl.endswith(".log"):
                continue

            filepath = os.path.join(self.log_dir, fayl)
            vozrast = self._vozrast_fayla(filepath)

            if vozrast >= STARYE_POSLE_DNEY:
                try:
                    archive_path = self._szhať_fayl(filepath)
                    arhivirovano.append((fayl, vozrast, archive_path))
                    print(f"✓ Архивирован: {fayl} ({vozrast} дней)")
                except Exception as e:
                    print(f"! Ошибка при архивации {fayl}: {e}")

        if not arhivirovano:
            print("Файлов для архивации не найдено")

        return arhivirovano

    def spisok_arkhivov(self):
        # выводим список всех архивов
        fayly = [f for f in os.listdir(self.archive_dir) if f.endswith(".gz")]

        if not fayly:
            print("Архивов нет")
            return []

        print(f"\nАрхивы ({len(fayly)}):")
        for f in sorted(fayly):
            path = os.path.join(self.archive_dir, f)
            razmer = os.path.getsize(path) / 1024
            print(f"  {f} ({razmer:.1f} КБ)")

        return fayly