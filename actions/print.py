from bot import bot, get_inline_keyboard
from generator import generate_printable_json
from pdf import pdf
from actions.start import start
from sql import delete_from_queue

@bot.message_handler(commands=['print'])
def handle_print(msg):
    print_pdf(msg)


def print_pdf(msg):
    bot.delete_message(msg.chat.id, msg.message_id)
    user_id = msg.chat.id
    delete_from_queue(user_id)
    json = generate_printable_json(user_id)
    if json != '[]':
        path = pdf.create_pdf(json, user_id)
        doc = open(path, 'rb')
        bot.send_document(user_id, doc)
        start(msg)
    else:
        message = 'Очередь печати пуста'
        buttons = [('❌ Закрыть', 'start=0')]
        keyboard = get_inline_keyboard(buttons)
        bot.send_message(msg.chat.id, text=message, reply_markup=keyboard, parse_mode='Markdown')