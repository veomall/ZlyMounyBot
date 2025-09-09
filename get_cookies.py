import getpass
import os
import asyncio
from twikit import Client
from dotenv import load_dotenv

load_dotenv()

cookies_path = os.getenv("COOKIES_PATH", "cookies.json")

async def main():
    if os.path.exists(cookies_path):
        overwrite = input(
            f"Файл '{cookies_path}' уже существует. Перезаписать? (y/n): "
        ).lower()
        if overwrite != 'y':
            print("Операция отменена.")
            return

    username = input("Введите ваш логин (username) в Твиттере: ")
    email = input("Введите вашу почту (email), привязанную к аккаунту: ")
    password = getpass.getpass("Введите ваш пароль: ")

    client = Client('ru-RU')

    try:
        await client.login(
            auth_info_1=username,
            auth_info_2=email,
            password=password
        )

        client.save_cookies(cookies_path)
        
        print(f"\n[УСПЕХ] Авторизация прошла успешно.")
        print(f"Сессия сохранена в файл: {cookies_path}")

    except Exception as e:
        print(f"\n[ОШИБКА] {e}")
        print("Пожалуйста, проверьте ваши данные или наличие 2FA.")


if __name__ == '__main__':
    asyncio.run(main())
