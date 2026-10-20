# Log Monitor

Внутренний инструмент мониторинга лог-файлов сервера.

## Установка
python monitor.py

## Использование
# показать сводку за день
python monitor.py server.log

# фильтровать только ошибки
python monitor.py server.log ERROR

## Формат лог-файла
2026-10-20 08:32:00 ERROR [auth-service] Failed to connect
2026-10-20 09:47:00 WARN [db] Connection pool almost full
2026-10-20 10:54:00 INFO [api] Request processed successfully

## Уровни логирования
ERROR / WARN / INFO / DEBUG