import pandas as pd
import plotly.graph_objects as go
import datetime
start_time = datetime.datetime.now()
df = pd.read_csv('US_Accidents_Dec19.csv')
end_time = datetime.datetime.now()
print(f'csv read in {end_time - start_time}')
df = df.head(500000)
fig = go.Figure(go.Scattergeo(lat=df.Start_Lat, lon=df.Start_Lng, marker_color=df.Severity,
                                 mode='markers'))
fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=180)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()