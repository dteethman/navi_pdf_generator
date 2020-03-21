from telebot import TeleBot, apihelper, types
from config import TOKEN, PROXY
import sql

apihelper.proxy = PROXY
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['add'])
def handle_message(msg):
    sql.delete_from_queue(msg.chat.id)
    sql.insert_row('print_queue', {"user_id": msg.chat.id, "is_active": 1})
