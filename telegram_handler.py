from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_ADMIN_CHAT_ID

# Глобальная переменная для экземпляра твиттер-клиента
twitter_client_instance = None
# Словарь для хранения состояний пользователей (ожидание кастомного ответа)
# {user_id: tweet_id}
user_states = {}

def set_twitter_client(client):
    global twitter_client_instance
    twitter_client_instance = client

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id == TELEGRAM_ADMIN_CHAT_ID:
        await update.message.reply_text("Привет! Я готов к работе.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    action, tweet_id = query.data.split('|')

    if action == 'reply_dove':
        success = twitter_client_instance.reply_to_tweet(tweet_id, "🕊️")
        status = "✅ Ответ 🕊️ отправлен." if success else "❌ Ошибка отправки."
        await query.edit_message_text(text=f"{query.message.text}\n\n---\n{status}")

    elif action == 'reject':
        await query.edit_message_text(text=f"{query.message.text}\n\n---\n🚫 Отклонено.")

    elif action == 'custom_reply':
        user_id = query.from_user.id
        user_states[user_id] = tweet_id
        await query.message.reply_text("Введите ваш вариант ответа на этот твит:")
        await query.edit_message_text(text=f"{query.message.text}\n\n---\n✍️ Ожидаю ваш текст...")


async def handle_custom_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_states:
        tweet_id = user_states.pop(user_id) # Получаем ID и удаляем состояние
        custom_text = update.message.text
        
        await update.message.reply_text(f"Отправляю ваш ответ на твит {tweet_id}...")
        success = twitter_client_instance.reply_to_tweet(tweet_id, custom_text)
        status = "✅ Ваш ответ отправлен." if success else "❌ Ошибка отправки."
        await update.message.reply_text(status)
    else:
        # Если бот не ожидает ответа, можно добавить стандартное поведение
        pass

async def send_for_approval(tweet):
    """Отправляет твит на модерацию в Telegram."""
    tweet_link = f"https://twitter.com/{tweet.author.username}/status/{tweet.id}"
    
    keyboard = [
        [InlineKeyboardButton("Ответить 🕊️", callback_data=f'reply_dove|{tweet.id}')],
        [InlineKeyboardButton("Написать свой вариант ✍️", callback_data=f'custom_reply|{tweet.id}')],
        [InlineKeyboardButton("Отклонить ❌", callback_data=f'reject|{tweet.id}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_text = (
        f"Обнаружен длинный твит (>5 слов).\n\n"
        f"**Автор:** {tweet.author.name} (@{tweet.author.username})\n"
        f"**Текст:**\n{tweet.text}\n\n"
        f"🔗 **Ссылка:** {tweet_link}"
    )
    
    # context.bot.send_message(...)
    await application.bot.send_message(
        TELEGRAM_ADMIN_CHAT_ID,
        message_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Создаем приложение
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_callback))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_reply))