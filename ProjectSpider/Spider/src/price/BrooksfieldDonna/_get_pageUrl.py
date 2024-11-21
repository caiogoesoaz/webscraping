# Import JSON module
import json
import pandas as pd
import glob
import os


marca = 'BrooksfieldDonna'
_f = glob.glob(f"src\\price\\{marca}\\json_*.json")
files = [(f, os.path.basename(f).split('_')[2].split('.')[0]) for f in _f]

def extract_json(file):
  # Opening JSON file
  with open(file, encoding='utf-8') as json_file:
    data = json.load(json_file)
    df = pd.json_normalize(data['itemListElement'])
    df = df[['item.name','item.@id']]
    df = df.rename(columns={'item.name': "nome", 'item.@id': "url"})

  return df

dfs = []
for c in files:
  _df = extract_json(c[0])
  _df['marca'] = marca
  _df['catalogo'] = c[1]
  _df['flg_crawled'] = 0
  dfs.append(_df)

df = pd.concat(dfs)
df.to_excel(f'src/price/{marca}/to_crawl.xlsx', index=False)