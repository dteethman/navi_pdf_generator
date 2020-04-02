from bot import bot, get_inline_keyboard
from actions import add, show, clear, print


@bot.message_handler(commands=['start'])
def handle_start(msg):
    bot.delete_message(msg.chat.id, msg.message_id)
    start(msg)


def start(msg):
    user_id = msg.chat.id
    buttons = [
        ('➕ Добавить', 'start=1'),
        ('👀 Посмореть очередь', 'start=2'),
        ('🖨 Напечатать', 'start=3'),
        ('🗑 Очистить', 'start=4'),
        ('❌ Выйти', 'start=5'),
    ]

    bot.send_message(user_id, text='Это навигационноценникопечатательный бот. \nЧто будем делать?', reply_markup=get_inline_keyboard(buttons))


@bot.callback_query_handler(func=lambda call: call.data.startswith('start'))
def handle_action(call):
    msg = call.message
    action = int(call.data.split('=')[-1])
    if action == 1:
        add.add_to_queue(msg)
    elif action == 2:
        show.show(msg)
    elif action == 3:
        print.print_pdf(msg)
    elif action == 4:
        clear.ask_clear(msg)
    elif action == 5:
        bot.delete_message(msg.chat.id, msg.message_id)
    elif action == 0:
        start(msg)
        bot.delete_message(msg.chat.id, msg.message_id)
