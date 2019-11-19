import pandas as pd
import currency_data
import datetime

currency_data.main()
df = pd.read_csv(currency_data.filename,index_col=(0,1),header=0)
# print(df.loc[df.index.get_level_values(1)=='GBP'])
for base in df.index.levels[1]:
    df.loc[df.index.get_level_values(1)==base].to_csv(f'test_{base}.csv')
