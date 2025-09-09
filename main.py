import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

from twitter_client import TwitterBotClient
import telegram_handler
import database
from grammar_checker import check_text_stub

async def main_cycle():
    database.init_db()
    
    twitter_bot = TwitterBotClient()
    await twitter_bot.connect()
    
    telegram_handler.set_twitter_client(twitter_bot)
    
    check_interval = int(os.getenv("CHECK_INTERVAL_SECONDS", 300))
    
    print("[Main] Бот запущен и готов к работе.")

    while True:
        last_seen_id = database.get_last_seen_tweet_id()
        new_tweets = await twitter_bot.get_new_tweets_since(last_seen_id)
        
        if new_tweets:
            latest_tweet_id = new_tweets[0].id
            database.set_last_seen_tweet_id(latest_tweet_id)
            print(f"[Main] Найдено {len(new_tweets)} новых твитов. Новый last_id: {latest_tweet_id}")
            
            for tweet in reversed(new_tweets):
                check_result = check_text_stub(tweet.text)
                if check_result.is_flagged:
                    print(f"[Main] Твит {tweet.id} отправлен на модерацию: {check_result.reason}")
                    # await telegram_handler.send_for_approval(tweet)
        else:
            print("[Main] Новых твитов не найдено.")
        
        print(f"[Main] Проверка завершена. Следующая через {check_interval} секунд.")
        await asyncio.sleep(check_interval)

async def main():
    # print("[Telegram] Запускаю Telegram-бота...")
    # await telegram_handler.application.initialize()
    # await telegram_handler.application.start()
    # await telegram_handler.application.updater.start_polling()
    # print("[Telegram] Telegram-бот запущен.")

    await main_cycle()

    # print("[Telegram] Останавливаю Telegram-бота...")
    # await telegram_handler.application.updater.stop()
    # await telegram_handler.application.stop()
    # await telegram_handler.application.shutdown()
    # print("[Telegram] Telegram-бот остановлен.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n[Main] Бот остановлен.")
    except Exception as e:
        print(f"[Main] Произошла критическая ошибка: {e}")