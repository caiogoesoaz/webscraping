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
def get_product_list():

  sleep(5)

  # Lista de Produtos
  _css = "li.product-item"
  product_items = driver.find_elements(By.CSS_SELECTOR, _css)
  
  # Extrair url
  _list = []
  for item in product_items:
    # for DEBUG
    # print(item.get_attribute('innerHTML'))

    # URL do Produto
    _css = "a"
    _element_url = item.find_element(By.CSS_SELECTOR, _css)
    # print(_element_url.get_attribute('innerHTML'))
    product_url = _element_url.get_attribute('href')
    print(product_url)
    _list.append(product_url)

  return _list

# Cralwer da pagina
def to_crawl(driver, dpto, categoria, url):
  print(url)

  # Inicializar
  driver.get(url)
  sleep(5)

  # Inicializar as variáveis
  pages=0
  product_list=[]

  # Carregar todas as paginas
  while True:
    try:
      
      # Limite no numero de paginas
      print(pages)
      if pages >= 30: break

      try:

        # Ir até o final da pagina para carregar
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        sleep(3)

        pages = pages + 1
      
      except:
        pages = 99

    except Exception as e:
      print(f"An error occurred: {e}")
      print(driver.page_source)
      driver.quit()

  # Extrair as informações
  _list = get_product_list()
  product_list = product_list + _list
    
  # Retorna as informações
  return [[dpto, categoria, l] for l in product_list]


if __name__ == "__main__":
  marca = "Alcaçuz"
  # Lista de paginas
  catalogos = [
    # ['feminino','Blusas','https://www.alcacuz.com.br/roupas-alcacuz/blusas.html'],
    ['feminino','Camisas','https://www.alcacuz.com.br/roupas-alcacuz/camisas.html'],
    ['feminino','Calcas','https://www.alcacuz.com.br/roupas-alcacuz/calcas.html'],
    ['feminino','Casacos','https://www.alcacuz.com.br/roupas-alcacuz/casacos.html'],
    ['feminino','Tricots','https://www.alcacuz.com.br/roupas-alcacuz/tricots.html'],
    ['feminino','Saias','https://www.alcacuz.com.br/roupas-alcacuz/saias.html'],
    ['feminino','Macacoes','https://www.alcacuz.com.br/roupas-alcacuz/macacoes.html'],
    ['feminino','Vestidos','https://www.alcacuz.com.br/roupas-alcacuz/vestidos.html']
  ]

  for c in catalogos:
    data = to_crawl(driver, *c)

    df = pd.DataFrame(data, columns =['dpto', 'categoria','product_url'], dtype = str)
    df.to_excel(f'src/price/{marca}/crawl_{c[0]}_{c[1]}.xlsx', index=False)

  driver.quit()