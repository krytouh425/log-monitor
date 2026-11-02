# Модуль экспорта — сохраняем записи лога в разные форматы
# Используется для передачи данных в другие системы мониторинга

import csv
import json
import os
from datetime import datetime

EXPORT_DIR = "exports"  # папка для экспортированных файлов


class ExporterLoga:
    def __init__(self, zapisi, export_dir=EXPORT_DIR):
        self.zapisi = zapisi
        self.export_dir = export_dir
        self._sozdat_papku()

    def _sozdat_papku(self):
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def _imya_fayla(self, format):
        vremya = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.export_dir, f"log_export_{vremya}.{format}")

    def v_csv(self):
        # экспортируем в CSV для анализа в Excel
        fayl = self._imya_fayla("csv")
        with open(fayl, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Время", "Уровень", "Источник", "Сообщение"])
            for z in self.zapisi:
                writer.writerow([
                    z.vremya.strftime("%Y-%m-%d %H:%M:%S"),
                    z.uroven,
                    z.istochnik or "",
                    z.soobshenie
                ])
        print(f"✓ Экспортировано в CSV: {fayl}")
        return fayl

    def v_json(self):
        # экспортируем в JSON для автоматической обработки
        fayl = self._imya_fayla("json")
        with open(fayl, "w", encoding="utf-8") as f:
            json.dump(
                [z.to_dict() for z in self.zapisi],
                f,
                ensure_ascii=False,
                indent=2
            )
        print(f"✓ Экспортировано в JSON: {fayl}")
        return fayl

    def tolko_oshibki(self):
        # экспортируем только ошибки для разбора инцидентов
        oshibki = [z for z in self.zapisi if z.uroven == "ERROR"]
        if not oshibki:
            print("Ошибок в логе не найдено")
            return None

        fayl = self._imya_fayla("txt")
        with open(fayl, "w", encoding="utf-8") as f:
            f.write(f"ОШИБКИ ИЗ ЛОГА — {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
            f.write("=" * 50 + "\n\n")
            for z in oshibki:
                f.write(f"{z.vremya.strftime('%H:%M:%S')} ")
                if z.istochnik:
                    f.write(f"[{z.istochnik}] ")
                f.write(f"{z.soobshenie}\n")

        print(f"✓ Ошибки экспортированы: {fayl}")
        return fayl