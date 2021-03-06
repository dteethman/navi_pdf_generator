from telebot import TeleBot, types
from config import TOKEN

bot = TeleBot(TOKEN)
print(TOKEN)

def get_inline_keyboard(buttons):
    keyboard = types.InlineKeyboardMarkup()
    for button in buttons:
        keyboard.add(types.InlineKeyboardButton(text=button[0], callback_data=button[1]))
    return keyboard
