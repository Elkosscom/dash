import requests
import datetime as dt

bases = ['GBP','EUR','USD','PLN']
date_range = dt.timedelta(365)
start_date=str(dt.date.today()-date_range)
end_date=str(dt.date.today())

for base in bases:
    r = requests.get(f'https://api.exchangeratesapi.io/history?start_at={start_date}&end_at={end_date}&base={base}')
    print(r.content)