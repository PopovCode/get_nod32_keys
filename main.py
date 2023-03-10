from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import os
import time
import config
import re
import sqlite3


def save_links_to_file(links):
    file_path = 'tmp/links.txt'
    with open(file_path, 'a', encoding='utf-8') as file:
        for link in links:
            file.write(link)
            file.write('\n')
    print(f'[INFO] - Links saved to file({file_path})')


def clear_tmp_folder():
    tmp_path = "tmp/"
    tmp_files = os.listdir(tmp_path)
    for tmp_f in tmp_files:
        os.remove(os.path.join(tmp_path, tmp_f))
    print('[INFO] - Temp folder is cleaning.... OK!')


def get_keys_from_file(tmp_path):
    files_list = os.listdir(tmp_path)
    sample = r'\b\w{4}\b-\w{4}-\w{4}-\w{4}-\w{4}\b'
    result = []
    for file in files_list:
        with open(f'{tmp_path}/{file}', 'r', encoding='utf-8') as f:
            text = f.read()
            keys = re.findall(sample, text)
            result.extend(keys)

    return result


def get_html_page_get_out_webbrowser():
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()))
    jump_to_the_right_section(driver, url=config.URL,
                              login=config.LOGIN, password=config.PASSWORD)
    click_all_hedden_content_buttons(driver)
    save_html_to_file(driver)
    driver.quit()


def save_html_to_file(driver):
    file_path = 'tmp/index.html'
    html = driver.page_source
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'[INFO] - HTML saved to file({file_path})')


def parsing_links_from_downloaded_html():
    file_html_path = 'tmp/index.html'
    print(f'[INFO] - Start parsing {file_html_path}')
    with open(file_html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    links = []
    hidden_blocs = soup.find_all('blockquote', class_="ipsBlockquote built")
    for item in hidden_blocs:
        link = item.find('pre', class_='prettyprint').text.strip()
        links.append(link)

    print(f'[INFO] - Parsing {file_html_path} complete!')
    return links


def jump_to_the_right_section(driver, url, login, password):
    # Load page1
    driver.get(url=url)
    WebDriverWait(driver=driver, timeout=10).until(
        EC.presence_of_element_located((By.ID, "footer_utilities")))
    # Find and click login button
    driver.find_element(By.XPATH, '//*[@id="sign_in"]').click()
    time.sleep(2)
    # Fill login and pass
    driver.find_element(By.XPATH, '//*[@id="ips_username"]').send_keys(login)
    driver.find_element(
        By.XPATH, '//*[@id="ips_password"]').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="login"]/div[5]/input').click()
    WebDriverWait(driver=driver, timeout=10).until(
        EC.presence_of_element_located((By.ID, "footer_utilities")))
    # Go to section
    driver.find_element(
        By.XPATH, '//*[@id="category_36"]/div/div/div/div/table/tbody/'
        + 'tr[2]/td[2]/h4/strong/a').click()
    WebDriverWait(driver=driver, timeout=10).until(
        EC.presence_of_element_located((By.ID, "footer_utilities")))
    # Go to NOD32 topic
    driver.find_element(By.XPATH, '//*[@id="tid-link-47660"]').click()
    time.sleep(2)
    # Go to last page from topic
    driver.find_element(
        By.XPATH, '//*[@id="content"]/div[2]/div/ul[3]/li[2]').click()


def click_all_hedden_content_buttons(driver):
    buttons = driver.find_elements(By.CLASS_NAME, 'bbc_spoiler_show')
    for button in buttons:
        button.click()
        time.sleep(1)


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print('[INFO]: Connect to database....OK\n')

    except sqlite3.Error as error:
        print('[INFO]: Connect to database....ERROR\n', error)

    return conn


def add_links_to_db(sqlite_connection, links):
    cursor = sqlite_connection.cursor()
    for link in links:
        if check_key_from_db(sqlite_connection=sqlite_connection, link=link):
            sql_insert_query = f"""
            insert into keys (key_link) values ('{link}')
            """
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


def main():
    get_html_page_get_out_webbrowser()
    links = parsing_links_from_downloaded_html()

    sqlite_connection = create_connection(db_file=config.DB_FILE)
    add_links_to_db(sqlite_connection=sqlite_connection, links=links)

    if sqlite_connection:
        sqlite_connection.close()
    print('\n[INFO]: Close connect to database....OK')

    clear_tmp_folder()


if __name__ == "__main__":
    main()
