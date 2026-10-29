# Модуль статистических отчётов — анализируем лог за период
# Используется дежурным администратором в конце смены

from datetime import datetime
from collections import Counter


class StatsReporter:
    def __init__(self, zapisi):
        self.zapisi = zapisi

    def po_chasam(self):
        # считаем количество записей по часам
        schetchik = Counter()
        for z in self.zapisi:
            chas = z.vremya.hour
            schetchik[chas] += 1
        return dict(sorted(schetchik.items()))

    def po_istochnikam(self):
        # считаем записи по сервисам
        schetchik = Counter()
        for z in self.zapisi:
            istochnik = z.istochnik or "неизвестно"
            schetchik[istochnik] += 1
        return dict(schetchik.most_common())

    def samyy_aktivnyy_chas(self):
        po_chasam = self.po_chasam()
        if not po_chasam:
            return None
        return max(po_chasam, key=po_chasam.get)

    def vyvesti_otchet(self):
        print("\n" + "=" * 50)
        print("  СТАТИСТИКА ЛОГА")
        print("=" * 50)
        print(f"  Всего записей: {len(self.zapisi)}")

        po_urovnyam = Counter(z.uroven for z in self.zapisi)
        print("\n  По уровням:")
        for uroven in ("ERROR", "WARN", "INFO", "DEBUG"):
            kolichestvo = po_urovnyam.get(uroven, 0)
            print(f"    {uroven}: {kolichestvo}")

        aktivnyy_chas = self.samyy_aktivnyy_chas()
        if aktivnyy_chas is not None:
            print(f"\n  Самый активный час: {aktivnyy_chas}:00")

        print("\n  По сервисам:")
        for istochnik, count in self.po_istochnikam().items():
            print(f"    {istochnik}: {count}")

        print("=" * 50 + "\n")