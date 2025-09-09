import os
from twikit import Client

class TwitterBotClient:
    def __init__(self):
        self.client = Client('ru-RU')
        self._is_connected = False

    async def connect(self):
        cookies_path = os.getenv('COOKIES_PATH')
        if not cookies_path or not os.path.exists(cookies_path):
            raise FileNotFoundError(
                f"Файл куки не найден по пути '{cookies_path}'. "
                "Убедитесь, что переменная COOKIES_PATH в .env указана верно "
                "и файл существует."
            )
        try:
            self.client.load_cookies(cookies_path)
            me = await self.client.user()
            print(f"[Twitter] Успешно вошел в аккаунт: {me.name} (@{me.screen_name})")
            self._is_connected = True
        except Exception as e:
            print(f"[Twitter] Ошибка при загрузке сессии: {e}")
            raise

    async def get_new_tweets_since(self, last_id: str | None, limit=200):
        if not self._is_connected:
            raise ConnectionError("Клиент твиттера не подключен.")
        
        if not last_id:
            return await self.client.get_latest_timeline()
        
        print(f"[Twitter] Ищу твиты новее {last_id}...")
        try:
            is_scrolling = True
            new_tweets = []
            while is_scrolling:
                tweets_list = await self.client.get_latest_timeline()
                if not tweets_list:
                    return []

                for tweet in tweets_list:
                    if len(new_tweets) >= limit:
                        is_scrolling = False
                        break
                    if tweet.id == last_id:
                        is_scrolling = False
                        break
                    new_tweets.append(tweet)

            return new_tweets
        except Exception as e:
            print(f"[Twitter] Ошибка получения ленты: {e}")
            return []

    async def reply_to_tweet(self, tweet_id, text):
        if not self._is_connected:
            raise ConnectionError("Клиент твиттера не подключен.")
        try:
            await self.client.create_tweet(text, reply_to=tweet_id)
            print(f"[Twitter] Успешно ответил на твит {tweet_id}")
            return True
        except Exception as e:
            print(f"[Twitter] Ошибка при отправке ответа на твит {tweet_id}: {e}")
            return False