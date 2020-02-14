import pandas as pd
import datetime


df = pd.read_csv("novel-coronavirus - data_adm1.csv")
df.set_index(
    ["country", "location_id", "location", "latitude", "longitude"], inplace=True
)

new_cols = [col.split("_") for col in df.columns]
for i in range(len(new_cols)):
    new_cols[i][1] = datetime.datetime.strptime(new_cols[i][1], "%d-%m-%Y")

df.columns = pd.MultiIndex.from_tuples(new_cols)

df = df.swaplevel(i=0, j=1, axis=1)
df.columns = df.columns.to_flat_index()
# print(df)
df.reset_index(inplace=True)
# print(df)
