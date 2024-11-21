# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import json

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
# options.add_argument("--incognito")
options.add_argument("--start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])


driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10) 

# Cralwer da pagina
def to_crawl(driver, dpto, categoria, url):
  print(url)

  # Inicializar
  driver.get(url)
  sleep(10)

  # Inicializar as variáveis
  pages=0
  product_list=[]

  # Carregar todas as paginas
  while True:
    try:
      
      # Limite no numero de paginas
      print(pages)
      if pages >= 10: break

      try:
        # Botão de carregar
        xpath = "//button/div[contains(text(), 'Carregar mais produtos')]"

        # Localiza o botão da proxima pagina e centraliza
        button = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.execute_script("""
          var element = arguments[0];
          var elementRect = element.getBoundingClientRect();
          var absoluteElementTop = elementRect.top + window.pageYOffset;
          var middle = absoluteElementTop - (window.innerHeight / 2);
          window.scrollTo(0, middle);
        """, button)
        sleep(10)

        # Clica no botão
        button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        button.click()

        pages = pages + 1
      
      except:
        pages = pages + 1

    except Exception as e:
      print(f"An error occurred: {e}")
      driver.quit()

  soup = BeautifulSoup(driver.page_source, 'html.parser')
  script_tag = soup.find_all('script', type='application/ld+json')[1]

  if script_tag:
    # Extract the JSON data
    json_data = script_tag.string
    # Parse the JSON data
    data = json.loads(json_data)
  
  return data


if __name__ == "__main__":
  marca = "BrooksfieldDonna"
  # Lista de paginas
  catalogos = [
    ['feminino','Blazers','https://www.brooksdonna.com.br/roupas/categorias/blazer'],
    ['feminino','Blusa','https://www.brooksdonna.com.br/roupas/categorias/blusa'],
    ['feminino','Calça','https://www.brooksdonna.com.br/roupas/categorias/calca'],
    ['feminino','Camisa','https://www.brooksdonna.com.br/roupas/categorias/camisa'],
    ['feminino','Casaco','https://www.brooksdonna.com.br/roupas/categorias/casaco---jaqueta'],
    ['feminino','Casaqueto','https://www.brooksdonna.com.br/roupas/categorias/casaqueto'],
    ['feminino','Saia','https://www.brooksdonna.com.br/roupas/categorias/saia'],
    ['feminino','Shorts','https://www.brooksdonna.com.br/roupas/categorias/shorts'],
    ['feminino','Tshirt','https://www.brooksdonna.com.br/roupas/categorias/t-shirt---regata'],
    ['feminino','Vestido','https://www.brooksdonna.com.br/roupas/categorias/vestido---macacao']
  ]
  for c in catalogos:
    data = to_crawl(driver, *c)

    # Save the JSON data to a file
    with open(f'src/price/{marca}/json_{c[0]}_{c[1]}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

  driver.quit()