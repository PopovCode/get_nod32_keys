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


def save_links_to_file(links):
    with open('tmp/links.txt', 'a', encoding='utf-8') as file:
        for link in links:
            file.write(link)
            file.write('\n')
    print('[INFO] - Links saved to file')


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
    print('WebDriver complited!')
    driver.quit()


def get_download_links():
    with open('tmp/index.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    links = []
    hidden_blocs = soup.find_all('blockquote', class_="ipsBlockquote built")
    for item in hidden_blocs:
        link = item.find('pre', class_='prettyprint').text.strip()
        links.append(link)

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
        By.XPATH, '//*[@id="category_36"]/div/div/div/div/table/tbody/tr[2]/td[2]/h4/strong/a').click()
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


def save_html_to_file(driver):
    html = driver.page_source
    with open('tmp/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('File saved!')


def main():
    # keys = get_keys_from_file('tmp')
    # print(keys)
    get_html_page_get_out_webbrowser()
    links = get_download_links()
    save_links_to_file(links=links)
    # clear_tmp_folder()


if __name__ == "__main__":
    main()
