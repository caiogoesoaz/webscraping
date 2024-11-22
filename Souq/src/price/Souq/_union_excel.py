import pandas as pd
import glob
import os

marca = 'Souq'
_f = glob.glob(f"Souq\\src\\price\\{marca}\\excel_*.xlsx")

# Verifica se o nome do arquivo possui ao menos três partes após o split
files = [(f, os.path.basename(f).split('_')[2].split('.')[0]) for f in _f if len(os.path.basename(f).split('_')) > 2]

dfs = []
for c in files:
    _df = pd.read_excel(c[0])
    dfs.append(_df)

df = pd.concat(dfs, ignore_index=True)
df.to_excel(f'Souq/src/price/{marca}/products.xlsx', index=False)
