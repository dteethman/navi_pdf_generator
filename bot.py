from telebot import TeleBot, apihelper, types
from config import TOKEN, PROXY
import sql

apihelper.proxy = PROXY
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['add'])
def handle_message(msg):
    add_to_queue(msg)


def add_to_queue(msg):
    sql.delete_from_queue(msg.chat.id)
    sql.insert_row('print_queue', {'user_id': msg.chat.id, 'is_active': 1})
    zones = sql.get_zones()
    buttons = [(zone[1], f'zone_id={zone[0]}') for zone in zones]
    bot.send_message(msg.chat.id, text='Зона', reply_markup=get_inline_keyboard(buttons))
    bot.delete_message(msg.chat.id, msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('zone_id'))
def handle_zone(call):
    msg = call.message
    zone_id = int(call.data.split('=')[-1])
    sql.update('print_queue', {'zone_id': zone_id}, {'user_id': msg.chat.id, 'is_active': 1})
    categories = sql.get_categories(zone_id)
    buttons = [(cat[2], f'cat_id={cat[0]}') for cat in categories]

    row = sql.get_active_row(msg.chat.id)
    buttons.insert(0, ('<--', f"add=1"))

    bot.send_message(msg.chat.id, text='Категория', reply_markup=get_inline_keyboard(buttons))
    bot.delete_message(msg.chat.id, msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('cat_id'))
def handle_cat(call):
    msg = call.message
    cat_id = int(call.data.split('=')[-1])
    sql.update('print_queue', {'cat_id': cat_id}, {'user_id': msg.chat.id, 'is_active': 1})

    brands = sql.get_brands(cat_id)
    buttons = [(brand[2], f'brand_id={brand[0]}') for brand in brands]
    if sql.get_category(cat_id)[3]:
            buttons.insert(0, ('Без бренда', "brand_id=0"))

    row = sql.get_active_row(msg.chat.id)
    buttons.insert(0, ('<--', f"zone_id={row[2]}"))

    bot.send_message(msg.chat.id, text='Бренд', reply_markup=get_inline_keyboard(buttons))
    bot.delete_message(msg.chat.id, msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('brand_id'))
def handle_brand(call):
    msg = call.message
    brand_id = int(call.data.split('=')[-1])
    if brand_id == 0:
        ask_quantity(msg)
        return
    sql.update('print_queue', {'brand_id': brand_id}, {'user_id': msg.chat.id, 'is_active': 1})
    models = sql.get_models(brand_id)
    buttons = [(model[1], f'model_id={model[0]}') for model in models]
    if sql.get_brand(brand_id)[3]:
        buttons.insert(0, ('Без модели', "model_id=0"))

    row = sql.get_active_row(msg.chat.id)
    buttons.insert(0, ('<--', f"cat_id={row[3]}"))

    bot.send_message(msg.chat.id, text='Модель', reply_markup=get_inline_keyboard(buttons))
    bot.delete_message(msg.chat.id, msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('model_id'))
def handle_model(call):
    msg = call.message
    model_id = int(call.data.split('=')[-1])
    if model_id == 0:
        ask_quantity(msg)
        return
    sql.update('print_queue', {'model_id': model_id}, {'user_id': msg.chat.id, 'is_active': 1})
    ask_quantity(msg)


def ask_quantity(msg):
    bot.register_next_step_handler(msg, handle_quantity)
    bot.send_message(msg.chat.id, text='Количество')
    bot.delete_message(msg.chat.id, msg.message_id)


def handle_quantity(msg):
    row = sql.get_active_row(msg.chat.id)
    sql.update('print_queue', {'quantity': int(msg.text), 'is_active': 0}, {'user_id': msg.chat.id, 'is_active': 1})
    buttons = [("Добавить еще", "add=1"), ("Достаточно", "add=0")]

    printable_data = generate_printable_data(row[0])
    message = f"Добавлено:\n*{printable_data[0]}* - {printable_data[1]} - {printable_data[2]} - {printable_data[3]} шт."

    bot.send_message(msg.chat.id, text=message, reply_markup=get_inline_keyboard(buttons), parse_mode="Markdown")
    bot.delete_message(msg.chat.id, msg.message_id)
    bot.delete_message(msg.chat.id, msg.message_id - 1)


@bot.callback_query_handler(func=lambda call: call.data.startswith('add'))
def handle_add_new(call):
    msg = call.message
    add = int(call.data.split('=')[-1])
    if add == 1:
        bot.delete_message(msg.chat.id, msg.message_id)
        add_to_queue(msg)
    else:
        bot.delete_message(msg.chat.id, msg.message_id)


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

    return (zone_str, category_str, model_str, quantity)

def get_inline_keyboard(buttons):
    keyboard = types.InlineKeyboardMarkup()
    for button in buttons:
        keyboard.add(types.InlineKeyboardButton(text=button[0], callback_data=button[1]))
    return keyboard
