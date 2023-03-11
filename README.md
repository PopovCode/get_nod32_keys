# Parser NOD32 keys

## Get started:

#### 1. Установить зависимости
    poetry install

#### 2. Создать файл config.py:
    URL = 'https://philka.ru/forum'
    LOGIN = 'you_login'
    PASSWORD = 'you_password'
    DB_FILE = './you_db.sqlite3'
    PARSING_INDEX_HTML_PATH = './tmp/index.html'

#### 3. Создать папку tmp:
    mkdir tmp

#### 4. Запуск
    poetry shell
    python3 main.py
