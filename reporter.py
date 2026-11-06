# Модуль отчётов — формируем детальный отчёт по логу за смену
# Используется дежурным администратором для передачи следующей смене

import os
from datetime import datetime
from collections import Counter


class ReporterSmeny:
    def __init__(self, zapisi, smena="день"):
        self.zapisi = zapisi
        self.smena = smena
        self.vremya = datetime.now()

    def _statistika_po_chasam(self):
        schetchik = Counter(z.vremya.hour for z in self.zapisi)
        return dict(sorted(schetchik.items()))

    def _top_oshibok(self, top=5):
        oshibki = [z for z in self.zapisi if z.uroven == "ERROR"]
        schetchik = Counter(z.soobshenie[:60] for z in oshibki)
        return schetchik.most_common(top)

    def sohranit_v_fayl(self, filepath=None):
        if not filepath:
            vremya_str = self.vremya.strftime("%Y%m%d_%H%M")
            filepath = f"report_{vremya_str}.txt"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("=" * 55 + "\n")
            f.write(f"  ОТЧЁТ СМЕНЫ — {self.smena.upper()}\n")
            f.write(f"  Сформирован: {self.vremya.strftime('%d.%m.%Y %H:%M')}\n")
            f.write("=" * 55 + "\n\n")

            # общая статистика
            po_urovnyam = Counter(z.uroven for z in self.zapisi)
            f.write(f"Всего записей: {len(self.zapisi)}\n")
            for uroven in ("ERROR", "WARN", "INFO", "DEBUG"):
                f.write(f"  {uroven}: {po_urovnyam.get(uroven, 0)}\n")

            # топ ошибок
            top = self._top_oshibok()
            if top:
                f.write("\nЧасто повторяющиеся ошибки:\n")
                for soobshenie, count in top:
                    f.write(f"  {count}x {soobshenie}\n")

            # активность по часам
            f.write("\nАктивность по часам:\n")
            for chas, count in self._statistika_po_chasam().items():
                f.write(f"  {chas:02d}:00 — {count} записей\n")

            f.write("\n" + "=" * 55 + "\n")

        print(f"✓ Отчёт смены сохранён: {filepath}")
        return filepath