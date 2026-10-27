# Модуль алертов — оповещаем команду о критических ошибках в логах
# Проверяет пороговые значения и формирует список срочных уведомлений

from datetime import datetime

# пороговые значения для алертов
MAX_OSHIBOK_V_CHAS = 10     # больше 10 ошибок в час — алерт
MAX_WARN_V_CHAS = 25        # больше 25 предупреждений в час — алерт


class MenedzherAlertov:
    def __init__(self, zapisi):
        self.zapisi = zapisi

    def _zapisi_za_posledniy_chas(self, uroven):
        # фильтруем записи за последний час нужного уровня
        seychas = datetime.now()
        return [
            z for z in self.zapisi
            if z.uroven == uroven
            and (seychas - z.vremya).seconds <= 3600
        ]

    def proverit_porogi(self):
        # проверяем не превышены ли пороговые значения
        oshibki = self._zapisi_za_posledniy_chas("ERROR")
        preduprezhdeniya = self._zapisi_za_posledniy_chas("WARN")

        alerty = []

        if len(oshibki) >= MAX_OSHIBOK_V_CHAS:
            alerty.append({
                "uroven": "CRITICAL",
                "soobshenie": f"За последний час {len(oshibki)} ошибок — превышен порог {MAX_OSHIBOK_V_CHAS}",
                "kolichestvo": len(oshibki)
            })

        if len(preduprezhdeniya) >= MAX_WARN_V_CHAS:
            alerty.append({
                "uroven": "WARNING",
                "soobshenie": f"За последний час {len(preduprezhdeniya)} предупреждений — превышен порог {MAX_WARN_V_CHAS}",
                "kolichestvo": len(preduprezhdeniya)
            })

        return alerty

    def chastye_oshibki(self, min_povtoreniy=3):
        # находим ошибки которые повторяются чаще всего
        schetchik = {}
        for z in self.zapisi:
            if z.uroven == "ERROR":
                klyuch = z.soobshenie[:50]  # первые 50 символов
                schetchik[klyuch] = schetchik.get(klyuch, 0) + 1

        # возвращаем только те что повторяются достаточно часто
        return {
            msg: count
            for msg, count in sorted(schetchik.items(), key=lambda x: x[1], reverse=True)
            if count >= min_povtoreniy
        }

    def pokazat_alerty(self):
        alerty = self.proverit_porogi()
        chastye = self.chastye_oshibki()

        if not alerty and not chastye:
            print("\n✓ Критических алертов нет\n")
            return

        if alerty:
            print("\n🚨 АЛЕРТЫ:")
            print("-" * 45)
            for a in alerty:
                print(f"  [{a['uroven']}] {a['soobshenie']}")

        if chastye:
            print("\n🔁 ЧАСТО ПОВТОРЯЮЩИЕСЯ ОШИБКИ:")
            print("-" * 45)
            for msg, count in chastye.items():
                print(f"  {count}x {msg}")

        print()