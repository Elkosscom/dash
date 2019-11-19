import requests
import datetime as dt
import pandas as pd
import ast
import os


def fetch_tables(base_list, start_at, end_at):
    """
    Sends a request to exchangeratesapi.io and saves gathered data as pandas dataframe with columns as target currency
    and (date,base_currency) as index
    :param base_list: three letter codes list for base currencies, for example ["GBP", "EUR", "USD", "PLN"]
    :param start_at: 'YYYY-MM-DD' string, selects starting date for currency rates
    :param end_at: 'YYYY-MM-DD' string, selects end date for currency rates
    :return: pd.DataFrame
    """
    df_return = pd.DataFrame()
    for base in base_list:
        r = requests.get(
            f"https://api.exchangeratesapi.io/history?start_at={start_at}&end_at={end_at}&base={base}"
        )
        content = ast.literal_eval(r.content.decode("utf-8"))
        df = pd.DataFrame.from_dict(content["rates"], orient="index")
        df["base"] = base
        df.reset_index(inplace=True)
        df.set_index(["index", "base"], inplace=True)
        df.sort_index(level=0, inplace=True)
        df_return = df_return.append(df, sort=False)
    return df_return.drop_duplicates()


bases = ["GBP", "EUR", "USD", "PLN"]
date_range = dt.timedelta(365)
start_date = str(dt.date.today() - date_range)
end_date = str(dt.date.today())
filename = f"currency_{dt.date.today()}.csv"

def main():

    if f"currency_{dt.date.today()}.csv" in os.listdir():
        pass
    else:
        for file in os.listdir(os.getcwd()):
            print(file)
            if file.lower().endswith('.csv'):
                os.remove(file)
        df = fetch_tables(bases, start_date, end_date)
        df.to_csv(f"currency_{dt.date.today()}.csv")


if __name__ == "__main__":
    main()
