from bot import bot, get_inline_keyboard, generate_printable_data
import sql


@bot.message_handler(commands=['show'])
def handle_show(msg):
    queue = sql.get_queue(msg.chat.id)
    q_ids = [q[0] for q in queue]
    data = [generate_printable_data(q_id) for q_id in q_ids]

    message = ''
    for i, d in enumerate(data):
        message += f"{i+1}) *{d['zone']}* - {d['category']} - " \
                  f"{d['title']} - {d['quantity']} шт.\n"
    buttons = [('Закрыть', 'show=0')]
    keyboard = get_inline_keyboard(buttons)

    bot.send_message(msg.chat.id, text=message, reply_markup=keyboard, parse_mode='Markdown')