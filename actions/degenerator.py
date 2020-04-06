from bot import bot, get_inline_keyboard
import sql


@bot.message_handler(commands=['degenerator'])
def handle_clear(msg):
    degenerate(msg)


def degenerate(msg):
    user_id = msg.chat.id
    sql.clear_queue(user_id)
    zones = sql.get_zones()

    for zone in zones:
        cats = sql.get_categories(zone[0])

        for cat in cats:
            brands = sql.get_brands(cat[0])

            for brand in brands:
                models = sql.get_models(brand[0])

                for model in models:
                    sql.insert_row('print_queue', {
                        'user_id': user_id,
                        'zone_id': zone[0],
                        'cat_id': cat[0],
                        'brand_id': brand[0],
                        'model_id': model[0],
                        'quantity': 1,
                        'is_active': 0,
                    })

                if brand[3] == 1:
                    sql.insert_row('print_queue', {
                        'user_id': user_id,
                        'zone_id': zone[0],
                        'cat_id': cat[0],
                        'brand_id': brand[0],
                        'model_id': None,
                        'quantity': 1,
                        'is_active': 0,
                    })

            if cat[4] == 1:
                sql.insert_row('print_queue', {
                    'user_id': user_id,
                    'zone_id': zone[0],
                    'cat_id': cat[0],
                    'brand_id': None,
                    'model_id': None,
                    'quantity': 1,
                    'is_active': 0,
                })
