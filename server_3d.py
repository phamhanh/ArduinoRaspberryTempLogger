import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px# load data
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#df = pd.read_csv('log_20221218_2000.txt') # make plot
#df_long=pd.melt(df, id_vars=['time'], value_vars=['a0','a2','a3','a4','a5','a6'])
#fig = px.plot(df_long, y='value', x="time", title='Temperature', color='variable')

import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Read data from a csv
df = pd.read_csv('temp.csv') # make plot


fig = go.Figure(data=[go.Surface(z=df.values)])

fig.update_layout(title='Mt Bruno Elevation',
                  width=900, height=900,
                  margin=dict(l=65, r=50, b=65, t=90))


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])# set app layout
app.layout = html.Div(children=[
    html.H1('Test Dash App', style={'textAlign':'center'}),
    html.Br(),
    dcc.Dropdown(
        options=[{'label': i, 'value': i} for i in df.columns],
        value='a0',
        id='dropdown',
        style={"width": "50%", "offset":1,},
        clearable=False,
    ),
    dcc.Graph(id='histogram', figure=fig)
])
if __name__ == "__main__":
    app.run_server(debug=True)
