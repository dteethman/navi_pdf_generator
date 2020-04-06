from bot import bot, get_inline_keyboard
import sql


@bot.message_handler(commands=['clear'])
def handle_clear(msg):
    ask_clear(msg)


def ask_clear(msg):
    user_id = msg.chat.id
    bot.delete_message(msg.chat.id, msg.message_id)
    buttons = [('Да', 'clear=1'), ('Нет', 'clear=0')]
    keyboard = get_inline_keyboard(buttons)
    count = len(sql.get_queue(user_id))
    if count != 0:
        message = f'Сейчас в очереди *{count} позиций*\n' \
                  f'Очистить очередь печати?'

        bot.send_message(user_id, text=message, reply_markup=keyboard, parse_mode='Markdown')
    else:
        message = 'Очередь печати пуста'
        buttons = [('❌ Закрыть', 'start=0')]
        keyboard = get_inline_keyboard(buttons)
        bot.send_message(msg.chat.id, text=message, reply_markup=keyboard, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data.startswith('clear'))
def handle_clear(call):
    msg = call.message
    clear = int(call.data.split('=')[-1])

    if clear == 1:
        sql.clear_queue(msg.chat.id)
        bot.delete_message(msg.chat.id, msg.message_id)
        message = 'Очередь печати очищена'
        buttons = [('❌ Закрыть', 'start=0')]
        keyboard = get_inline_keyboard(buttons)
        bot.send_message(msg.chat.id, text=message, reply_markup=keyboard, parse_mode='Markdown')
    else:
        bot.delete_message(msg.chat.id, msg.message_id)
        message = 'Очистка отменена'
        buttons = [('❌ Закрыть', 'start=0')]
        keyboard = get_inline_keyboard(buttons)
        bot.send_message(msg.chat.id, text=message, reply_markup=keyboard, parse_mode='Markdown')
