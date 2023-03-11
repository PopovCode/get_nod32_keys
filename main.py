import config
import db
import downloader
import parser


def main():
    sqlite_connection = db.create_connection(db_file=config.DB_FILE)
    try:
        downloader.get_html_page_get_out_webbrowser()
        links = parser.parsing_links_from_downloaded_html(config.PARSING_INDEX_HTML_PATH)
        db.add_links_to_db(sqlite_connection=sqlite_connection, links=links)

        # links = downloader.get_all_links_where_key_text_is_null(
        #     sqlite_connection=sqlite_connection)
        # for link in links:
        #     print(link[1])
        #     download_file_key(link=link[1])
    except Exception as e:
        print(e)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
        print('\n[INFO]: Close connect to database....OK')
        # clear_tmp_folder()


if __name__ == "__main__":
    main()

# Обновление записи
# update keys set key_text = 'PopovCode' where key_link like "%https://www.upload.ee/files/15002426/Key.txt.html%"

# Выбрать все ссылки у которых еще не скачан ключ
# select * from keys WHERE key_text is null
