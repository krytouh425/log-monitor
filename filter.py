# Модуль фильтрации — выбираем нужные записи из лога
# Используется для поиска конкретных событий и ошибок

from datetime import datetime


class FiltrLoga:
    def __init__(self, zapisi):
        self.zapisi = zapisi

    def po_urovnyu(self, uroven):
        # фильтруем по уровню ERROR / WARN / INFO / DEBUG
        return [z for z in self.zapisi if z.uroven == uroven.upper()]

    def po_istochniku(self, istochnik):
        # фильтруем по названию сервиса
        istochnik = istochnik.lower()
        return [
            z for z in self.zapisi
            if z.istochnik and istochnik in z.istochnik.lower()
        ]

    def po_klyuchevomu_slovu(self, slovo):
        # ищем записи содержащие ключевое слово
        slovo = slovo.lower()
        return [z for z in self.zapisi if slovo in z.soobshenie.lower()]

    def po_vremeni(self, s_chasa, do_chasa):
        # фильтруем по диапазону часов
        return [
            z for z in self.zapisi
            if s_chasa <= z.vremya.hour < do_chasa
        ]

    def neskolko_filtrov(self, uroven=None, istochnik=None, slovo=None):
        # комбинированная фильтрация по нескольким критериям
        rezultat = self.zapisi
        if uroven:
            rezultat = [z for z in rezultat if z.uroven == uroven.upper()]
        if istochnik:
            rezultat = [z for z in rezultat if z.istochnik and istochnik.lower() in z.istochnik.lower()]
        if slovo:
            rezultat = [z for z in rezultat if slovo.lower() in z.soobshenie.lower()]
        return rezultat

    def vyvesti(self, zapisi, zagolovok="РЕЗУЛЬТАТЫ ФИЛЬТРАЦИИ"):
        if not zapisi:
            print("Записей не найдено")
            return

        # считаем статистику по уровням
        po_urovnyam = {}
        for z in zapisi:
            po_urovnyam[z.uroven] = po_urovnyam.get(z.uroven, 0) + 1

        print(f"\n{'=' * 50}")
        print(f"  {zagolovok} ({len(zapisi)} записей)")
        print(f"  Уровни: " + " | ".join(f"{k}:{v}" for k, v in po_urovnyam.items()))
        print(f"{'=' * 50}")
        for z in zapisi:
            print(f"  {z}")
        print(f"{'=' * 50}\n")