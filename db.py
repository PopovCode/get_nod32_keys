import sqlite3


def create_connection(db_file: str) -> sqlite3.Connection:
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print('[INFO]: Connect to database....OK\n')

    except sqlite3.Error as error:
        print('[INFO]: Connect to database....ERROR\n', error)

    return conn


def add_links_to_db(sqlite_connection, links: list) -> None:
    cursor = sqlite_connection.cursor()
    for link in links:
        if check_key_from_db(sqlite_connection=sqlite_connection, link=link):
            sql_insert_query = f"insert into keys (key_link) values ('{link}')"
            cursor.execute(sql_insert_query)
            sqlite_connection.commit()
            print(f'[INFO]: Ссылка {link} добавлена в db')
        else:
            print(f'[INFO]: Ссылка {link} уже есть в базе')
            continue
    cursor.close()


def get_all_keys_from_db(sqlite_connection):
    cursor = sqlite_connection.cursor()
    sql_select = 'select * from keys'
    cursor.execute(sql_select)
    res = cursor.fetchall()
    cursor.close()
    return res


def check_key_from_db(sqlite_connection, link):
    cursor = sqlite_connection.cursor()
    sql = f'select * from keys where key_link = "{link}"'
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        return False
    return True


def get_all_links_where_key_text_is_null(sqlite_connection):
    cursor = sqlite_connection.cursor()
    sql_select = 'select * from keys WHERE key_text is null'
    cursor.execute(sql_select)
    res = cursor.fetchall()
    cursor.close()
    return res


def get_all_links_where_key_text_is_null(sqlite_connection):
    cursor = sqlite_connection.cursor()
    sql_select = 'select * from keys WHERE key_text is null'
    cursor.execute(sql_select)
    res = cursor.fetchall()
    cursor.close()
    return res
