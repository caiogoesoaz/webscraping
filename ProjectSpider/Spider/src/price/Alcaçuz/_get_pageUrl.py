# Import JSON module
import json
import pandas as pd
import glob
import os


marca = 'Alcaçuz'
_f = glob.glob(f"src\\price\\{marca}\\excel_*.xlsx")
files = [(f, os.path.basename(f).split('_')[2].split('.')[0]) for f in _f]

def extract_xlsx(file):
  # Concatenate xlsx files
  df = pd.read_excel(file)
  df['nome'] = ''
  df = df[['nome','product_url']]
  df = df.rename(columns={'item.name': "nome", 'product_url': "url"})

  return df

dfs = []
for c in files:
  _df = extract_xlsx(c[0])
  _df['marca'] = marca
  _df['catalogo'] = c[1]
  _df['flg_crawled'] = 0
  dfs.append(_df)

df = pd.concat(dfs)
df.to_excel(f'src/price/{marca}/to_crawl.xlsx', index=False)