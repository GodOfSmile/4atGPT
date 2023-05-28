from telegram import Update
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler
import openai
import os

load_dotenv()

# Установите свой API-ключ и идентификатор модели OpenAI
openai.api_key = os.getenv('API_KEY')
model_id = 'gpt-3.5-turbo'

def start_handler_fn(update: Update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text="Привет! Я бот, готовый помочь вам.")

def message_handler_fn(update: Update, context):
    chat_id = update.message.chat_id
    message_text = update.message.text

    # Отправляем запрос на сервер OpenAI Chat API
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=[
            {"role": "system", "content": "Вы: /start"},
            {"role": "user", "content": message_text},
        ]
    )

    # Извлекаем ответ из ответа сервера OpenAI Chat API
    bot_response = response.choices[0].message.content

    # Отправляем ответ пользователю
    context.bot.send_message(chat_id=chat_id, text=bot_response)

def main():
    # Установите свой токен доступа бота Telegram
    bot_token = '6089023026:AAF0EQBOYfyy4dHXyGcPx6m0aYiVkcOEoaQ'
    
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start_handler_fn)
    message_handler = MessageHandler(None, message_handler_fn)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
 main()