import telebot
import traceback


def send_message_to_channel(bot_token, chat_id, message):
    """
    Отправляет сообщение в телеграм канал, бот должен быть администратором канала
    chat_id - часть ссылки на телеграм канал с @, пример - @link_yandex_task
    """
    bot = telebot.TeleBot(bot_token)
    try:
        bot.send_message(chat_id=chat_id, text=message)
    except:
        traceback.print_exc()
        return False
    return True













