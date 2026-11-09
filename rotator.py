# Модуль ротации логов — управляем размером и количеством лог-файлов
# Используется для предотвращения переполнения диска на продакшене

import os
import shutil
from datetime import datetime


MAKS_RAZMER_MB = 50       # максимальный размер файла в МБ
MAKS_KOLICHESTVO = 10     # максимум файлов в ротации
PREDUPREZHDENIE_MB = 40   # предупреждение при достижении 40 МБ

class RotatorLogov:
    def __init__(self, filepath):
        self.filepath = filepath
        self.papka = os.path.dirname(filepath) or "."
        self.imya = os.path.basename(filepath)

    def _razmer_mb(self):
        if not os.path.exists(self.filepath):
            return 0
        return os.path.getsize(self.filepath) / (1024 * 1024)

    def nuzhen_povorot(self):
        # проверяем нужна ли ротация
        return self._razmer_mb() >= MAKS_RAZMER_MB

    def vypolnit_povorot(self):
        if not os.path.exists(self.filepath):
            print("Лог-файл не найден")
            return

        # переименовываем текущий файл с временной меткой
        vremya = datetime.now().strftime("%Y%m%d_%H%M%S")
        novoe_imya = os.path.join(self.papka, f"{self.imya}.{vremya}")
        shutil.move(self.filepath, novoe_imya)
        print(f"✓ Лог ротирован: {novoe_imya}")

        self._udalit_starye()

    def _udalit_starye(self):
        # оставляем только последние MAKS_KOLICHESTVO файлов
        fayly = sorted([
            f for f in os.listdir(self.papka)
            if f.startswith(self.imya + ".")
        ])

        while len(fayly) > MAKS_KOLICHESTVO:
            udalit = os.path.join(self.papka, fayly.pop(0))
            os.remove(udalit)
            print(f"✓ Удалён старый лог: {udalit}")

    def status(self):
        razmer = self._razmer_mb()
        print(f"\n{'=' * 40}")
        print(f"  СТАТУС РОТАЦИИ")
        print(f"  Файл: {self.filepath}")
        print(f"  Размер: {razmer:.1f} МБ / {MAKS_RAZMER_MB} МБ")
        print(f"  Нужна ротация: {'Да' if self.nuzhen_povorot() else 'Нет'}")
        print(f"{'=' * 40}\n")