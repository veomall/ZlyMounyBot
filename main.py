import asyncio
from config import CHECK_INTERVAL_SECONDS
from twitter_client import TwitterBotClient
from grammar_checker import check_text_stub
import telegram_handler
import database

async def main_cycle():
    # Инициализация
    database.init_db()
    twitter_bot = TwitterBotClient()
    telegram_handler.set_twitter_client(twitter_bot)
    
    print("Бот запущен...")

    while True:
        print("Начинаю проверку...")
        last_seen_id = database.get_last_seen_tweet_id()
        
        # Получаем новые твиты, они уже отсортированы от новых к старым
        new_tweets = twitter_bot.get_new_tweets_since(last_seen_id)
        
        if new_tweets:
            # Сразу обновляем ID самого свежего твита
            latest_tweet_id = new_tweets[0].id
            database.set_last_seen_tweet_id(latest_tweet_id)
            print(f"Найдено {len(new_tweets)} новых твитов. Новый last_id: {latest_tweet_id}")
            
            # Идем по списку в обратном порядке, чтобы обрабатывать от старых к новым
            for tweet in reversed(new_tweets):
                check_result = check_text_stub(tweet.text)
                if check_result.is_flagged:
                    print(f"Твит {tweet.id} отправлен на модерацию: {check_result.reason}")
                    await telegram_handler.send_for_approval(tweet)
        else:
            print("Новых твитов не найдено.")
        
        print(f"Проверка завершена. Следующая через {CHECK_INTERVAL_SECONDS} секунд.")
        await asyncio.sleep(CHECK_INTERVAL_SECONDS)

async def main():
    # Запускаем телеграм-бота в фоновом режиме
    await telegram_handler.application.initialize()
    await telegram_handler.application.start()
    await telegram_handler.application.updater.start_polling()

    # Запускаем основной цикл твиттер-бота
    await main_cycle()

    # Корректно останавливаем телеграм-бота при завершении
    await telegram_handler.application.updater.stop()
    await telegram_handler.application.stop()
    await telegram_handler.application.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")