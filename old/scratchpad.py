import pandas as pd
import currency_data
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
currency_data.main()
# df_currency_mini = pd.read_csv(currency_data.filename,index_col=(0,1),header=0)
# # print(df_currency_mini.loc[df_currency_mini.index.get_level_values(1)=='GBP'])
# # for base in df_currency_mini.index.levels[1]:
# #     df_currency_mini.loc[df_currency_mini.index.get_level_values(1)==base].to_csv(f'test_{base}.csv')
# # print(df_currency_mini.tail())
# last_date = df_currency_mini.index.levels[0][-1]
# a = [[x, x+1, x+2] for x in range(4)]
# print(a)
table_currencies = ["EUR", "USD", "PLN", 'GBP']
df = pd.read_csv(currency_data.filename, index_col=(0, 1), header=0)

curr_last_date = df.index.levels[0][-1]
df_c = df.loc[
    (df.index.get_level_values(1).isin(currency_data.bases))
    & (df.index.get_level_values(0) == curr_last_date)
]
df_c = pd.DataFrame(df_c.droplevel(0))
# print(df_currency_mini.droplevel(0))
df2 = pd.DataFrame()
dit = {}

for curr in ["EUR", "USD", "PLN"]:
    dit[curr] = {'Buy':df_c.at[curr,'GBP'],'Sell':df_c.at['GBP',curr]}

df2 = pd.DataFrame.from_dict(dit,orient='index')
df = df2.round(5).reset_index().rename(columns={"index": "Currency"})
# print(df_currency_mini)
# print(df_currency_mini.iloc[0]['Currency'])


df3 = pd.read_csv(currency_data.filename, index_col=(0, 1), header=0)
selected = [{'row': 0, 'column': 1, 'column_id': 'Buy'}, {'row': 1, 'column': 2, 'column_id': 'Sell'}]

def update_graph_currency(selection):
    fig = go.Figure()
    for item in selection:
        if item['column'] == 1:
            base = df.iloc[item['row']]['Currency']
            target = 'GBP'
        elif item['column'] == 2:
            base = 'GBP'
            target = df.iloc[item['row']]['Currency']
        else:
            base='GBP'
            target='GBP'
        fig.add_trace(
            go.Scatter(
                x=df3[df3.index.get_level_values(1)==base].index.get_level_values(0),
                y=df3[df3.index.get_level_values(1)==base][target],
                name=f'{target}/{base}',
                mode='lines'
            )
        )
    fig.show()

print(df3[df3.index.get_level_values(1)=='GBP']['PLN'].values)

# update_graph(selected)
