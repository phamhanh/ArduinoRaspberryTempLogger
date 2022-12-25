import pandas as pd
import plotly.graph_objects as go # or plotly.express as px
import dash
from dash import dcc
from dash import html

df = pd.read_csv('temp.csv')

fig = go.Figure(go.Scatter(x = df['time'], y = df['54'], name='A0'))
#fig.add_trace(go.Scatter(x = df['time'], y = df['55'], name='A1'))# Faulty Sensor
fig.add_trace(go.Scatter(x = df['time'], y = df['57'], name='A3'))
fig.add_trace(go.Scatter(x = df['time'], y = df['56'], name='A2 Cooler')) 
fig.add_trace(go.Scatter(x = df['time'], y = df['58'], name='A4 Heater'))
fig.add_trace(go.Scatter(x = df['time'], y = df['59'], name='A5'))
#fig.add_trace(go.Scatter(x = df['time'], y = df['60'], name='A6')) # Faulty Sensor
#fig.add_trace(go.Scatter(x = df['time'], y = df['61'], name='A7')) # Faulty Sensor
fig.add_trace(go.Scatter(x = df['time'], y = df['62'], name='A8'))
fig.add_trace(go.Scatter(x = df['time'], y = df['63'], name='A9'))
fig.add_trace(go.Scatter(x = df['time'], y = df['64'], name='A10'))
fig.add_trace(go.Scatter(x = df['time'], y = df['65'], name='A11'))
fig.add_trace(go.Scatter(x = df['time'], y = df['66'], name='A12'))
fig.add_trace(go.Scatter(x = df['time'], y = df['67'], name='A13'))
fig.add_trace(go.Scatter(x = df['time'], y = df['68'], name='A14'))
fig.add_trace(go.Scatter(x = df['time'], y = df['69'], name='A15 Tempeh'))


fig.update_layout(title='Tempeh',
                   plot_bgcolor='rgb(230, 230,230)',
                   showlegend=True)

fig.show()

# fig.add_trace( ... )
# fig.update_layout( ... )



app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=True) 