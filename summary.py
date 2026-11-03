# Модуль сводки — формируем краткий отчёт о состоянии системы
# Используется дежурным администратором в начале и конце смены

from datetime import datetime
from collections import Counter


class SvodkaSmeny:
    def __init__(self, zapisi):
        self.zapisi = zapisi
        self.vremya_sozdaniya = datetime.now()

    def kolichestvo_po_urovnyam(self):
        return Counter(z.uroven for z in self.zapisi)

    def samye_aktivnye_sluzhby(self, top=5):
        # топ сервисов по количеству записей
        schetchik = Counter(
            z.istochnik for z in self.zapisi if z.istochnik
        )
        return schetchik.most_common(top)

    def kriticheskiy_period(self):
        # час с наибольшим количеством ошибок
        oshibki_po_chasam = Counter(
            z.vremya.hour for z in self.zapisi if z.uroven == "ERROR"
        )
        if not oshibki_po_chasam:
            return None
        return max(oshibki_po_chasam, key=oshibki_po_chasam.get)

    def sformirovat(self):
        urovni = self.kolichestvo_po_urovnyam()
        sluzhby = self.samye_aktivnye_sluzhby()
        kritich_chas = self.kriticheskiy_period()

        print(f"\n{'=' * 50}")
        print(f"  СВОДКА СМЕНЫ")
        print(f"  Сформирована: {self.vremya_sozdaniya.strftime('%d.%m.%Y %H:%M')}")
        print(f"  Всего записей: {len(self.zapisi)}")
        print(f"{'=' * 50}")

        print("\n  По уровням:")
        for uroven in ("ERROR", "WARN", "INFO", "DEBUG"):
            print(f"    {uroven}: {urovni.get(uroven, 0)}")

        if sluzhby:
            print("\n  Топ активных сервисов:")
            for sluzhba, count in sluzhby:
                print(f"    {sluzhba}: {count} записей")

        if kritich_chas is not None:
            print(f"\n  Критический период: {kritich_chas}:00 — {kritich_chas+1}:00")

        est_problemy = urovni.get("ERROR", 0) > 0
        print(f"\n  Статус смены: {'⚠️  ЕСТЬ ПРОБЛЕМЫ' if est_problemy else '✓ НОРМА'}")
        print(f"{'=' * 50}\n")