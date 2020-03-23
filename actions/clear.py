from bot import bot, get_inline_keyboard
import sql


@bot.message_handler(commands=['clear'])
def handle_clear(msg):
    buttons = [('Да', 'clear=1'), ('Нет', 'clear=0')]
    keyboard = get_inline_keyboard(buttons)

    count = len(sql.get_queue(msg.chat.id))

    if count != 0:
        message = f'Cейчас в очереди *{count} позиций*\n' \
                  f'Отчистить очередь печати?'

        bot.send_message(msg.chat.id, text=message, reply_markup=keyboard, parse_mode='Markdown')
    else:
        bot.send_message(msg.chat.id, text='Очередь печати пуста')


@bot.callback_query_handler(func=lambda call: call.data.startswith('clear'))
def handle_clear(call):
    msg = call.message
    clear = int(call.data.split('=')[-1])

    if clear == 1:
        sql.clear_queue(msg.chat.id)
        bot.delete_message(msg.chat.id, msg.message_id)
    else:
        bot.delete_message(msg.chat.id, msg.message_id)
