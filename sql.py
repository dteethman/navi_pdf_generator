import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)


def execute(query, data=None):
    cursor = conn.cursor()
    if data:
        cursor.execute(query, data)
    else:
        cursor.execute(query)
    conn.commit()
    return cursor


def executemany(query, data):
    cursor = conn.cursor()
    cursor.executemany(query, data)
    conn.commit()
    return cursor


def insert_row(table: str, cols: dict):
    names = ','.join(list(cols.keys()))
    count = ('?,' * len(cols.keys()))[:-1]
    values = tuple(cols.values())
    return execute(f'INSERT INTO {table} ({names}) VALUES ({count})', values)


def update(table: str, cols: dict, where: dict):
    set = ','.join([f'{col}=?' for col, value in cols.items()])
    keys = ' AND '.join([f'{key}=?' for key, value in where.items()])
    values = list(cols.values()) + list(where.values())
    return execute(f'UPDATE {table} SET {set} WHERE {keys}', tuple(values))


def delete(table: str, where: str, equal):
    try:
        return execute(f'DELETE FROM {table} WHERE {where}=?', (equal,))
    except sqlite3.OperationalError as err:
        print(f'Ошибка: {err}')


def get_active_row(user_id):
    return execute('SELECT * FROM print_queue WHERE user_id=? AND is_active=1', (user_id,)).fetchone()


def get_zones() -> list:
    return execute('SELECT * FROM zones ORDER BY zone ASC').fetchall()


def get_zone(zone_id) -> tuple:
    return execute('SELECT * FROM zones WHERE id=?', (zone_id,)).fetchone()


def get_categories(zone_id: int) -> list:
    return execute(
        'SELECT id, category, display_name, print_name, is_final FROM categories '
        'JOIN categories_to_zones ON id = categories_to_zones.cat_id '
        'WHERE categories_to_zones.zone_id = ? '
        'ORDER BY display_name',
        (zone_id,)).fetchall()


def get_category(cat_id) -> tuple:
    return execute('SELECT * FROM categories WHERE id=?', (cat_id,)).fetchone()


def get_brands(cat_id: int) -> list:
    return execute(
        'SELECT id, brand, display_name, is_final, is_ignored FROM brands '
        'JOIN brands_to_categories ON id = brands_to_categories.brand_id '
        'WHERE brands_to_categories.cat_id = ? '
        'ORDER BY display_name',
        (cat_id,)).fetchall()


def get_brand(brand_id) -> tuple:
    return execute('SELECT * FROM brands WHERE id=?', (brand_id,)).fetchone()


def get_models(brand_id: int) -> list:
    return execute(
        'SELECT id, model FROM models '
        'JOIN models_to_brands ON id = models_to_brands.model_id '
        'WHERE models_to_brands.brand_id = ? '
        'ORDER BY model',
        (brand_id,)).fetchall()


def get_model(model_id) -> tuple:
    return execute('SELECT * FROM models WHERE id=?', (model_id,)).fetchone()


def add_to_queue(cols: dict, user_id):
    pass


def delete_from_queue(user_id):
    try:
        return execute(f'DELETE FROM print_queue WHERE user_id=? AND is_active=1', (user_id,))
    except sqlite3.OperationalError as err:
        print(f'Ошибка: {err}')


def get_from_queue_by_id(queue_id):
    return execute('SELECT * FROM print_queue WHERE id=?', (queue_id,)).fetchone()


def clear_queue(user_id):
    return delete('print_queue', 'user_id', user_id)


def get_queue(user_id):
    return execute('SELECT * FROM print_queue WHERE user_id=? ', (user_id,)).fetchall()


if __name__ == '__main__':
    print(get_zones())
    print(get_categories(1))
    print(get_brands(1))
    print(get_models(1))
    print(get_models(3))
    # update('print_queue', {'zone_id': 1}, {'user_id': 359, 'is_active': 1})
    delete_from_queue(359)
    print(get_queue(219523490))