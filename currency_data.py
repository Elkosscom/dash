import requests
import datetime as dt
import pandas as pd

bases = ['GBP','EUR','USD','PLN']
date_range = dt.timedelta(365)
start_date=str(dt.date.today()-date_range)
end_date=str(dt.date.today())

# r = requests.get(f'https://api.exchangeratesapi.io/history?start_at={start_date}&end_at={end_date}&base={bases[0]}')
with open(r'history.json','rb') as r:
    df = pd.read_json(r.read()[9:-60],orient='index')
    df = pd.DataFrame(df)

print(df.transpose)