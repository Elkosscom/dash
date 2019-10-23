import openpyxl as xl
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


months = ('Jan','Feb','Mar')

wb = xl.open('data.xlsx',read_only=True,data_only=True)
ws = wb['Sales']
df = pd.read_excel('data.xlsx',sheet_name=1)
df['Month'] = pd.DatetimeIndex(df['Date']).month

print(df.head())

data_alpha = df.loc[df.Item == 'Alpha']
fig = px.bar(df,'Month','Net',color='Item',barmode='group')
fig.show()