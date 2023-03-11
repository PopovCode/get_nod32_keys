import os
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config


def get_html_page_get_out_webbrowser() -> None:
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()))
    try:
        go_to_last_page_topic(driver, url=config.URL,
                              login=config.LOGIN, password=config.PASSWORD)
        open_hidden_fields(driver)
        save_page_to_file(driver)
    except Exception as e:
        print(e)
    finally:
        driver.quit()


def go_to_last_page_topic(driver, url, login, password) -> None:
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


def open_hidden_fields(driver) -> None:
    buttons = driver.find_elements(By.CLASS_NAME, 'bbc_spoiler_show')
    for button in buttons:
        button.click()
        time.sleep(1)


def save_page_to_file(driver) -> None:
    file_path = 'tmp/index.html'
    html = driver.page_source
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'[INFO] - HTML saved to file({file_path})')


def download_file_key(link):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless=new')
    download_dir = os.getcwd() + "/tmp/"
    prefs = {'download.default_directory': f'{download_dir}'}
    chrome_options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)
    driver.get(url=link)
    WebDriverWait(driver=driver, timeout=10).until(
        EC.presence_of_element_located((By.ID, "d_l")))
    driver.find_element(By.XPATH, '//*[@id="d_l"]').click()
    time.sleep(5)
    driver.quit()
