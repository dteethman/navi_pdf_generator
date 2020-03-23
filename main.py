from bot import bot
import actions
import pkgutil
modules = []
for _, name, _ in pkgutil.iter_modules(actions.__path__):
    modules.append(name)
exec(f'from actions import {",".join(modules)}')

bot.polling(none_stop=True, interval=0)
