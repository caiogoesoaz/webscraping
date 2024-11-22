# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import requests

from time import sleep
import random

import pandas as pd

# Lista de User-Agents
USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
  "Mozilla/5.0 (X11;U; Linux i686; en-GB; rv:1.9.1) Gecko/20090624 Ubuntu/9.04 (jaunty) Firefox/3.5",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.2.20) Gecko/20110803 Firefox",
  ]
user_agent = random.choice(USER_AGENTS)

options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={user_agent}")

# Headless
# options.add_argument("--headless")

# For debug
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument("--incognito")
options.add_argument("--start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])


driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10) 

# Função para pegar a informação do produto
def get_page_list(url):

  driver.get(url)

  sleep(5)

  # Lista de Produtos
  _css = "nav.navigation > ul > li a"
  _pages = driver.find_elements(By.CSS_SELECTOR, _css)
  
  # Extrair url
  _list = []
  for _p in _pages:

    _url = _p.get_attribute('href')
    _name = _p.get_attribute('innerText')
    _list.append([_name, _url])

  return _list


if __name__ == "__main__":
  marca = "Souq"

  data = get_page_list('https://www.souqstore.com.br/')

  df = pd.DataFrame(data, columns =['lista', 'url'], dtype = str)
  df.to_excel(f'Souq/src/price/{marca}/pageList.xlsx', index=False)

  driver.quit()