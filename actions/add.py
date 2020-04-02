from bot import bot, get_inline_keyboard
from generator import generate_printable_data
import sql


@bot.message_handler(commands=['add'])
def handle_add(msg):
    add_to_queue(msg)


def add_to_queue(msg):
    sql.delete_from_queue(msg.chat.id)
    sql.insert_row('print_queue', {'user_id': msg.chat.id, 'is_active': 1})

    zones = sql.get_zones()

    buttons = [(zone[1], f'zone_id={zone[0]}') for zone in zones]
    buttons.insert(0, ('⬅️ Назад', f"start=0"))

    bot.send_message(msg.chat.id, text='Выбери зону', reply_markup=get_inline_keyboard(buttons))
    bot.delete_message(msg.chat.id, msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('zone_id'))
def handle_zone(call):
    msg = call.message
    bot.clear_step_handler(msg)
    zone_id = int(call.data.split('=')[-1])

    zone = sql.get_zone(zone_id)
    categories = sql.get_categories(zone_id)

    sql.update('print_queue',
               {'zone_id': zone_id, 'cat_id': None, 'brand_id': None, 'model_id': None},
               {'user_id': msg.chat.id, 'is_active': 1})

    buttons = [(cat[2], f'cat_id={cat[0]}') for cat in categories]
    buttons.insert(0, (f'⬅️ Выбор зоны', f"start=1"))
    keyboard = get_inline_keyboard(buttons)

    message = f'Зона *{zone[1]}* \nВыбери категорию'

    bot.send_message(msg.chat.id, text=message, reply_markup=keyboard, parse_mode='Markdown')
    bot.delete_message(msg.chat.id, msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('cat_id'))
def handle_cat(call):
    msg = call.message
    bot.clear_step_handler(msg)
    cat_id = int(call.data.split('=')[-1])
    row = sql.get_active_row(msg.chat.id)

    zone = sql.get_zone(row[2])
    category = sql.get_category(cat_id)
    brands = sql.get_brands(cat_id)

    sql.update('print_queue',
               {'cat_id': cat_id, 'brand_id': None, 'model_id': None},
               {'user_id': msg.chat.id, 'is_active': 1})

    buttons = [(brand[2], f'brand_id={brand[0]}') for brand in brands]
    if sql.get_category(cat_id)[3]:
        buttons.insert(0, ('Без бренда и модели', "brand_id=0"))
    buttons.insert(0, (f'⬅️ {category[2]}', f"zone_id={zone[0]}"))
    keyboard = get_inline_keyboard(buttons)

    message = f'Категория *{category[2]}* \nВыбери бренд'

    bot.send_message(msg.chat.id, text=message, reply_markup=keyboard, parse_mode='Markdown')
    bot.delete_message(msg.chat.id, msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('brand_id'))
def handle_brand(call):
    msg = call.message
    bot.clear_step_handler(msg)
    brand_id = int(call.data.split('=')[-1])
    row = sql.get_active_row(msg.chat.id)

    if brand_id == 0:
        ask_quantity(msg)
        return
    category = sql.get_category(row[3])
    brand = sql.get_brand(brand_id)
    models = sql.get_models(brand_id)

    sql.update('print_queue',
               {'brand_id': brand_id, 'model_id': None},
               {'user_id': msg.chat.id, 'is_active': 1})

    if len(models) != 0:
        buttons = [(model[1], f'model_id={model[0]}') for model in models]
        if sql.get_brand(brand_id)[3]:
            buttons.insert(0, ('Без модели', "model_id=0"))
        buttons.insert(0, (f'⬅ {brand[2]}', f"cat_id={category[0]}"))
        keyboard = get_inline_keyboard(buttons)

        message = f'Бренд *{brand[2]}*\nВыбери модель'

        bot.send_message(msg.chat.id, text=message, reply_markup=keyboard, parse_mode='Markdown')
    else:
        ask_quantity(msg)
    bot.delete_message(msg.chat.id, msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('model_id'))
def handle_model(call):
    msg = call.message
    bot.clear_step_handler(msg)
    model_id = int(call.data.split('=')[-1])

    if model_id == 0:
        ask_quantity(msg)
        return

    sql.update('print_queue', {'model_id': model_id}, {'user_id': msg.chat.id, 'is_active': 1})
    ask_quantity(msg)


def ask_quantity(msg):
    row = sql.get_active_row(msg.chat.id)
    zone = sql.get_zone(row[2])
    category = sql.get_category(row[3])
    brand = sql.get_brand(row[4]) if row[4] is not None else None
    model = sql.get_model(row[5]) if row[5] is not None else None

    message = ''
    keyboard = None

    if model is not None:
        message = "Модель "
        if brand[4] == 0:
            message += f'*{brand[2]} *'
        message += f'*{model[1]}*'
        keyboard = get_inline_keyboard([(f'⬅ {model[1]}', f'brand_id={brand[0]}')])
    elif brand is not None:
        message += f'Бренд *{brand[2]}*'
        keyboard = get_inline_keyboard([(f'⬅ {brand[2]}', f'brand_id={brand[0]}')])
    else:
        message += f'*Категория {category[2]}*'
        keyboard = get_inline_keyboard([(f'⬅ {category[2]}', f'cat_id={category[0]}')])

    message += '\nВведи количество'
    bot.register_next_step_handler(msg, handle_quantity)
    bot.send_message(msg.chat.id, text=message, reply_markup=keyboard, parse_mode='Markdown')
    bot.delete_message(msg.chat.id, msg.message_id)


def handle_quantity(msg):
    row = sql.get_active_row(msg.chat.id)
    try:
        quantity = int(msg.text)
        sql.update('print_queue', {'quantity': quantity, 'is_active': 0}, {'user_id': msg.chat.id, 'is_active': 1})
        buttons = [("Добавить еще", "start=1"), ("Достаточно", "start=0")]

        printable_data = generate_printable_data(row[0])
        message = f"Добавлено:\n*{printable_data['zone']}* - {printable_data['category']} - " \
                  f"{printable_data['title']} - {printable_data['quantity']} шт."

        bot.send_message(msg.chat.id, text=message, reply_markup=get_inline_keyboard(buttons), parse_mode="Markdown")
        bot.delete_message(msg.chat.id, msg.message_id)
        bot.delete_message(msg.chat.id, msg.message_id - 1)
    except Exception as e:
        ask_quantity(msg)
        bot.delete_message(msg.chat.id, msg.message_id)
        bot.delete_message(msg.chat.id, msg.message_id - 1)
