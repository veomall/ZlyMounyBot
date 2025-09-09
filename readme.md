```
python -m venv .venv
.venv\Scripts\activate
```

```
python get_cookies.py
```

Создать '.env' с полями:
```
TELEGRAM_BOT_TOKEN="0000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
TELEGRAM_ADMIN_CHAT_ID=0000000000

COOKIES_PATH="cookies.json"

CHECK_INTERVAL_SECONDS=300
DB_NAME="processed_tweets.db"
```

```
python main.py
```

Необходимо:
1. проверить и реализовать логику телеграм бота для модерации
2. реализовать проверку текста
3. реализовать более полный мониторинг и логирование