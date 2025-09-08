from twikit import Client
from config import TWITTER_USERNAME, TWITTER_EMAIL, TWITTER_PASSWORD

class TwitterBotClient:
    def __init__(self):
        self.client = Client("ru-RU") # Указываем язык
        try:
            self.client.login(
                auth_info_1=TWITTER_USERNAME,
                auth_info_2=TWITTER_EMAIL,
                password=TWITTER_PASSWORD
            )
        except Exception as e:
            # Здесь нужна обработка ошибки входа, например, через логгер
            print(f"Ошибка входа в Твиттер: {e}")
            raise

    def get_new_tweets_since(self, last_id: str | None, limit=200):
        """
        Собирает все новые твиты из ленты подписок, которые новее last_id.
        Использует пагинацию.
        """
        print(f"Ищу твиты новее {last_id}...")
        new_tweets = []
        
        try:
            # get_home_latest_timeline - это лента "Following"
            timeline = self.client.get_home_latest_timeline()
            
            # Пробегаем по страницам, пока не найдем старый твит или не достигнем лимита
            for tweet in timeline:
                if len(new_tweets) >= limit:
                    print(f"Достигнут лимит в {limit} твитов.")
                    break
                if tweet.id == last_id:
                    print("Нашел последний виденный твит. Сбор завершен.")
                    break
                
                new_tweets.append(tweet)
            
            # Если last_id не был указан (первый запуск), берем только последнюю пачку
            if not last_id and new_tweets:
                return new_tweets[:20] # Ограничиваем для первого запуска

            return new_tweets

        except Exception as e:
            print(f"Ошибка получения ленты: {e}")
            return []

    def reply_to_tweet(self, tweet_id, text):
        """Отвечает на указанный твит."""
        try:
            self.client.create_tweet(text, reply_to=tweet_id)
            print(f"Успешно ответил на твит {tweet_id}")
            return True
        except Exception as e:
            print(f"Ошибка при отправке ответа на твит {tweet_id}: {e}")
            return False
