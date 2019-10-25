import openpyxl as xl
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


months = ('Jan','Feb','Mar')

wb = xl.open('data.xlsx',read_only=True,data_only=True)
ws = wb['Sales']
df = pd.read_excel('data.xlsx',sheet_name=1)
df['Month'] = pd.DatetimeIndex(df['Date']).month


fig = px.bar(df,'Month','Net',barmode='group',color='Item',facet_col='Depo')
# fig.add_bar(df,'Month','Quantity',barmode='group',color='Item',facet_col='Depo')
fig.show()

