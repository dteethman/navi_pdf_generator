from telebot import TeleBot, apihelper, types
from config import TOKEN, PROXY
import sql

apihelper.proxy = PROXY
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['add'])
def handle_message(msg):
    sql.delete_from_queue(msg.chat.id)
    sql.insert_row('print_queue', {"user_id": msg.chat.id, "is_active": 1})
    buttons = [('Зона 1', 'zone_id=1'), ('Я пошутил', 'no')]
    bot.send_message(msg.chat.id, text='Зона?', reply_markup=get_inline_keyboard(buttons))


@bot.callback_query_handler(func=lambda call: call.data.startswith('zone_id'))
def handle_zone(call):
    zone_id = int(call.data.split('=')[-1])
    bot.send_message(call.message.chat.id, f'Добавляем зону {zone_id}')


def get_inline_keyboard(buttons):
    keyboard = types.InlineKeyboardMarkup()
    for button in buttons:
        keyboard.add(types.InlineKeyboardButton(text=button[0], callback_data=button[1]))
    return keyboard
