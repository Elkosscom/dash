import requests
import datetime as dt
import pandas as pd
import os


def parse_json(json):
    start = json.index(b"{", 1)
    end = json[::-1].index(b"}", 1)
    return json[start:-end]


def fetch_tables(df, base_list, start_at, end_at):
    for base in base_list:
        r = requests.get(
            f"https://api.exchangeratesapi.io/history?start_at={start_date}&end_at={end_date}&base={base}"
        )
        data = pd.read_json(parse_json(r.content))
        data["base"] = base
        df.append(data)


bases = ["GBP", "EUR", "USD", "PLN"]
date_range = dt.timedelta(365)
start_date = str(dt.date.today() - date_range)
end_date = str(dt.date.today())

filename = f"curr_{dt.date.today()}.json"


def main():
    if filename in os.listdir():
        pass
    else:
        for file in os.listdir():
            if file.endswith(".json"):
                os.remove(file)
        df_currency = pd.DataFrame()
        fetch_tables(
            df=df_currency, base_list=bases, start_at=start_date, end_at=end_date
        )
        df_currency.to_json(filename)


if __name__ == "__main__":
    main()
