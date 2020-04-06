import sql
import json


def generate_readable_data(queue_id):
    row = sql.get_from_queue_by_id(queue_id)
    zone_str = str(sql.get_zone(row[2])[1])
    category_str = str(sql.get_category(row[3])[2])
    brand = sql.get_brand(row[4])
    model = sql.get_model(row[5])
    quantity = int(row[6])
    icon = str(sql.get_zone(row[2])[2])

    model_str = ''
    if brand is not None and brand[5] == 0:
        model_str += f'{brand[2]} '
    if model is not None:
        model_str += f'{model[1]}'

    return {
        "icon": icon,
        "zone": zone_str,
        "title": model_str,
        "category": category_str,
        "quantity": quantity
    }


def generate_printable_data(queue_id):
    row = sql.get_from_queue_by_id(queue_id)
    zone_str = str(sql.get_zone(row[2])[1])
    category_str = str(sql.get_category(row[3])[2])
    brand = sql.get_brand(row[4])
    model = sql.get_model(row[5])
    quantity = int(row[6])
    icon = str(sql.get_zone(row[2])[2])

    model_str = ''
    if brand is not None and brand[5] == 0:
        model_str += f'{brand[3]} '
    if model is not None:
        model_str += f'{model[2]}'

    return {
        "icon": icon,
        "zone": zone_str,
        "title": model_str,
        "category": category_str,
        "quantity": quantity
    }


def generate_printable_json(user_id):
    queue = sql.get_queue(user_id)
    user_ids = [q[0] for q in queue]
    data = [generate_printable_data(user_id) for user_id in user_ids]
    return json.dumps(data)