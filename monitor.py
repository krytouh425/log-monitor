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

# Модуль чтения лога — парсит лог-файл построчно
# Поддерживает стандартный формат: ГГГГ-ММ-ДД ЧЧ:ММ:СС УРОВЕНЬ [источник] сообщение

import re
import os

FAYL_LOGA = "server.log"  # лог-файл сервера по умолчанию

# шаблон строки лога
SHABLON = re.compile(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"  # дата и время
    r"(ERROR|WARN|INFO|DEBUG)\s+"                   # уровень
    r"(?:\[(.+?)\]\s+)?"                            # источник (опционально)
    r"(.+)"                                         # сообщение
)


class ChitateLoga:
    def __init__(self, filepath=FAYL_LOGA):
        self.filepath = filepath

    def proverit_fayl(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Лог-файл не найден: {self.filepath}")
        if os.path.getsize(self.filepath) == 0:
            raise ValueError("Лог-файл пустой")

    def razobrat_stroku(self, stroka, nomer):
        # пробуем распарсить строку по шаблону
        stroka = stroka.strip()
        if not stroka:
            return None

        sovpadenie = SHABLON.match(stroka)
        if not sovpadenie:
            print(f"! Строка {nomer}: не соответствует формату, пропускаем")
            return None

        vremya_str, uroven, istochnik, soobshenie = sovpadenie.groups()

        try:
            vremya = datetime.strptime(vremya_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print(f"! Строка {nomer}: неверный формат времени, пропускаем")
            return None

        return LogZapis(vremya, uroven, soobshenie.strip(), istochnik)

    def zagruzit(self):
        self.proverit_fayl()
        zapisi = []

        with open(self.filepath, encoding="utf-8") as f:
            for nomer, stroka in enumerate(f, start=1):
                zapis = self.razobrat_stroku(stroka, nomer)
                if zapis:
                    zapisi.append(zapis)

        print(f"Загружено записей: {len(zapisi)}")
        return zapisi

# Модуль фильтрации и анализа — сортирует записи по уровню
# Формирует сводку за день с подсчётом ошибок и предупреждений

class AnalizatorLoga:
    def __init__(self, zapisi):
        self.zapisi = zapisi

    def filtr_po_urovnyu(self, uroven):
        # возвращаем только записи нужного уровня
        return [z for z in self.zapisi if z.uroven == uroven.upper()]

    def filtр_po_vremeni(self, s_chasa, do_chasa):
        # фильтруем записи по диапазону часов
        return [
            z for z in self.zapisi
            if s_chasa <= z.vremya.hour < do_chasa
        ]

    def gruppirovat_po_istochniku(self):
        # группируем ошибки по сервису — удобно для дежурного
        gruppy = {}
        for z in self.zapisi:
            klyuch = z.istochnik or "неизвестно"
            if klyuch not in gruppy:
                gruppy[klyuch] = []
            gruppy[klyuch].append(z)
        return gruppy

    def svodka_za_den(self):
        # главный отчёт — выводим статистику за текущий день
        oshibki = self.filtr_po_urovnyu("ERROR")
        preduprezhdeniya = self.filtr_po_urovnyu("WARN")
        info = self.filtr_po_urovnyu("INFO")
        debug = self.filtr_po_urovnyu("DEBUG")

        print("\n" + "=" * 50)
        print("  СВОДКА ЛОГА ЗА ДЕНЬ")
        print("=" * 50)
        print(f"  Всего записей:      {len(self.zapisi)}")
        print(f"  ERROR:              {len(oshibki)}")
        print(f"  WARN:               {len(preduprezhdeniya)}")
        print(f"  INFO:               {len(info)}")
        print(f"  DEBUG:              {len(debug)}")
        print("=" * 50)

        if oshibki:
            print("\n  ПОСЛЕДНИЕ ОШИБКИ:")
            for z in oshibki[-5:]:  # показываем последние 5
                print(f"  {z}")

        if preduprezhdeniya:
            print("\n  ПОСЛЕДНИЕ ПРЕДУПРЕЖДЕНИЯ:")
            for z in preduprezhdeniya[-3:]:
                print(f"  {z}")

        print()