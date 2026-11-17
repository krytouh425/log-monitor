# Конфигурация монитора — все настройки в одном месте
# Меняй здесь не трогая основной код монитора

# настройки файлов
FAYL_LOGA = "server.log"
KODIROVKA = "utf-8"
MAKS_RAZMER_FAYLA_MB = 100  # максимальный размер файла

# настройки архивации
ARCHIVE_DIR = "archive"
STARYE_POSLE_DNEY = 7       # архивируем файлы старше N дней

# настройки алертов
MAX_OSHIBOK_V_CHAS = 10     # порог ошибок для алерта
MAX_WARN_V_CHAS = 25        # порог предупреждений для алерта

# настройки ротации
MAKS_RAZMER_ROTATSII_MB = 50
MAKS_FAYLOV_ROTATSII = 10

# настройки watchdog
INTERVAL_PROVERKI_SEK = 5   # как часто проверяем лог

# уровни логирования
UROVNI = ("ERROR", "WARN", "INFO", "DEBUG")

# формат строки лога
FORMAT_VREMENI = "%Y-%m-%d %H:%M:%S"