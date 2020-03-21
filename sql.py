import sqlite3

conn = sqlite3.connect('database.db')


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


def update(table: str, cols: dict, where: dict):
    set = ','.join([f'{col}=?' for col, value in cols.items()])
    keys = ' AND '.join([f'{key}=?' for key, value in where.items()])
    values = list(cols.values()) + list(where.values())
    return execute(f'UPDATE {table} SET {set} WHERE {keys}', tuple(values))


def get_zones() -> list:
    return execute('SELECT * FROM zones').fetchall()


def get_categories(zone_id: int) -> list:
    return execute(
        'SELECT id, category, display_name, is_final FROM categories '
        'JOIN categories_to_zones ON id = categories_to_zones.cat_id '
        'WHERE categories_to_zones.zone_id = ?',
        (zone_id,)).fetchall()


def get_brands(cat_id: int) -> list:
    return execute(
        'SELECT id, brand, display_name, is_final FROM brands '
        'JOIN brands_to_categories ON id = brands_to_categories.brand_id '
        'WHERE brands_to_categories.cat_id = ?',
        (cat_id,)).fetchall()


def get_models(brand_id: int) -> list:
    return execute(
        'SELECT id, model FROM models '
        'JOIN models_to_brands ON id = models_to_brands.model_id '
        'WHERE models_to_brands.brand_id = ?',
        (brand_id,)).fetchall()


def add_to_queue(cols: dict, user_id):
    pass


if __name__ == '__main__':
    print(get_zones())
    print(get_categories(1))
    print(get_brands(1))
    print(get_models(1))
    print(get_models(3))
    update('print_queue', {'zone_id': 1}, {'user_id': 359, 'is_active': 1})
