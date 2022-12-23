import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px# load data
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import urllib.request
import numpy as np

# Read data from a csv
z_data = pd.read_csv('temp.csv')

fig = go.Figure(data=[go.Surface(z=z_data.values)])

fig.update_layout(title='Mt Bruno Elevation', autosize=False,
                  width=900, height=900,
                  margin=dict(l=65, r=50, b=65, t=90))


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])# set app layout
app.layout = html.Div(children=[
    dcc.Graph(id='histogram', figure=fig)
])
if __name__ == "__main__":
    app.run_server(debug=True)
