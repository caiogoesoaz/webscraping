# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import random
import pandas as pd
from unicodedata import normalize
import re
from time import sleep

# Lista de User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11;U; Linux i686; en-GB; rv:1.9.1) Gecko/20090624 Ubuntu/9.04 (jaunty) Firefox/3.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.2.20) Gecko/20110803 Firefox",
]
user_agent = random.choice(USER_AGENTS)

# Configuração do navegador
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={user_agent}")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument("--incognito")
options.add_argument("--start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)


def page_number(driver, url):
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    sleep(10)

    try:
        _path = "//ul[contains(@class, 'ds-plp-pagination')]//li"
        _number_list = driver.find_elements(By.XPATH, _path)
        _number = [x.get_attribute('innerText') for x in _number_list]
        int_list = [int(s) for s in _number if s.isdigit()]
        return max(int_list) if int_list else 1
    except Exception as e:
        print(f"Erro ao obter número de páginas: {e}")
        return 1


def get_products(driver, url):
    driver.get(url)
    sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    sleep(10)

    # Lista de Produtos
    _css = "div > div.ds-sdk-product-item"
    try:
        product_items = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, _css))
        )
    except Exception as e:
        print(f"Erro ao localizar itens de produto: {e}")
        return []

    _list = []
    for item in product_items:
        try:
            # URL do Produto
            _url = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

            # Nome do Produto
            try:
                _name = item.find_element(By.CSS_SELECTOR, 'div.ds-sdk-product-item__product-name').get_attribute('innerText')
            except Exception:
                _name = "Nome não encontrado"

            # Preço do Produto
            try:
                _price = item.find_element(By.CSS_SELECTOR, 'div.ds-sdk-product-price').get_attribute('innerText')
                _prices = re.findall(r"R\$\s*\d+,\d{2}", _price)
                _prices = [price.replace("R$", "").strip() for price in _prices]
            except Exception:
                _prices = ['', '']

            price_o = _prices[0] if len(_prices) > 0 else ''
            price_f = _prices[1] if len(_prices) > 1 else ''

            print(url, _name, _url, price_o, price_f)
            _list.append([url, _name, _url, price_o, price_f])
        except Exception as e:
            print(f"Erro ao processar produto: {e}")

    return _list


def crawl(driver, url, pages):
    product_list = []
    for p in range(1, pages + 1):
        _url = f'{url}?p={p}'
        _list = get_products(driver, _url)
        product_list.extend(_list)
    return product_list


if __name__ == "__main__":
    marca = "Souq"

    # Lista de páginas
    df_pages = pd.read_excel(f'Souq/src/price/{marca}/excel_pageList.xlsx')

    for idx, row in df_pages.iterrows():
        _list = row['lista']
        _url = row['url']

        _name = _list.lower().replace(' ', '_')
        _name = normalize('NFKD', _name).encode('ASCII', 'ignore').decode('ASCII')

        _max_page = page_number(driver, _url)

        data = crawl(driver, _url, _max_page)
        df = pd.DataFrame(data, columns=['page_number', 'product', 'product_url', 'price_original', 'price_actual'], dtype=str)
        df.insert(0, 'list_url', _url)
        df.insert(0, 'list', _list)
        df.to_excel(f'Souq/src/price/{marca}/excel_{idx}_{_name}.xlsx', index=False)

    driver.quit()