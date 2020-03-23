from bot import bot
from telebot import types
from flask import Flask, request
import actions
import pkgutil
import os


modules = []
for _, name, _ in pkgutil.iter_modules(actions.__path__):
    modules.append(name)
exec(f'from actions import {",".join(modules)}')

server = Flask(__name__)


@server.route('/', methods=['POST'])
def webhook():
    bot.process_new_updates([types.Update.de_json(request.stream.read().decode('utf-8'))])
    return '?', 200


server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))

