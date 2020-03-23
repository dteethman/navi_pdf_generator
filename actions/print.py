from bot import bot, get_inline_keyboard, generate_printable_data, generate_printable_json
import sql
from pdf import pdf


@bot.message_handler(commands=['print'])
def handle_print(msg):
    user_id = msg.chat.id
    json = generate_printable_json(user_id)
    if json != '[]':
        path = pdf.create_pdf(json, user_id)
        doc = open(path, 'rb')
        bot.send_document(user_id, doc)
    else:
        bot.send_message(user_id, text='Очередь печати пуста')