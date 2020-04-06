from bot import bot, get_inline_keyboard
from generator import generate_readable_data
import sql


@bot.message_handler(commands=['show'])
def handle_show(msg):
    show(msg)


def show(msg):
    bot.delete_message(msg.chat.id, msg.message_id)
    sql.delete_from_queue(msg.chat.id)
    queue = sql.get_queue(msg.chat.id)
    q_ids = [q[0] for q in queue]
    data = [generate_readable_data(q_id) for q_id in q_ids]
    message = ''
    if len(data) > 0:
        for i, d in enumerate(data):
            message += f"{i + 1}) *{d['zone']}* - {d['category']} - " \
                       f"{d['title']} - {d['quantity']} шт.\n"
    else:
        message += 'Очередь печати пуста'
    buttons = [('❌ Закрыть', 'start=0')]
    keyboard = get_inline_keyboard(buttons)
    bot.send_message(msg.chat.id, text=message, reply_markup=keyboard, parse_mode='Markdown')

