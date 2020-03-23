from telebot import TeleBot, apihelper, types
from config import TOKEN, PROXY
import sql
import json

apihelper.proxy = PROXY
bot = TeleBot(TOKEN)


def generate_printable_data(queue_id):
    row = sql.get_from_queue_by_id(queue_id)
    zone_str = str(sql.get_zone(row[2])[1])
    category_str = str(sql.get_category(row[3])[2])
    brand = sql.get_brand(row[4])
    model = sql.get_model(row[5])
    quantity = int(row[6])

    model_str = ''
    if brand is not None:
        model_str += str(brand[2])
    if model is not None:
        model_str += str(model[1])

    return {
        "icon": "icons/listen.png",
        "zone": zone_str,
        "title": model_str,
        "category": category_str,
        "quantity": quantity
    }


def generate_printable_json(user_id):
    queue = sql.get_queue(user_id)
    user_ids = [q[0] for q in queue]
    data = [generate_printable_data(user_id) for user_id in user_ids]
    return json.dumps(data)


def get_inline_keyboard(buttons):
    keyboard = types.InlineKeyboardMarkup()
    for button in buttons:
        keyboard.add(types.InlineKeyboardButton(text=button[0], callback_data=button[1]))
    return keyboard


if __name__ == '__main__':
    print(generate_printable_json(321391124))