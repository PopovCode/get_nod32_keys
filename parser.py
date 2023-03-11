import os
import re

from bs4 import BeautifulSoup


def parsing_links_from_downloaded_html(file_html_path: str) -> list:
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


def save_links_to_file(links: list) -> None:
    file_path = 'tmp/links.txt'
    with open(file_path, 'a', encoding='utf-8') as file:
        for link in links:
            file.write(link)
            file.write('\n')
    print(f'[INFO] - Links saved to file({file_path})')


def get_keys_from_file(tmp_path: str) -> list:
    files_list = os.listdir(tmp_path)
    sample = r'\b\w{4}\b-\w{4}-\w{4}-\w{4}-\w{4}\b'
    result = []
    for file in files_list:
        with open(f'{tmp_path}/{file}', 'r', encoding='utf-8') as f:
            text = f.read()
            keys = re.findall(sample, text)
            result.extend(keys)

    return result
