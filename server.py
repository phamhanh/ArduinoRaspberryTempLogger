import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px# load data
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv('log_20221218_2000.txt') # make plot
#df_long=pd.melt(df, id_vars=['time'], value_vars=['a0','a2','a3','a4','a5','a6'])
#fig = px.plot(df_long, y='value', x="time", title='Temperature', color='variable')

fig = make_subplots(rows=2, cols=3, start_cell="bottom-left",
    subplot_titles=("A0", "A2", "A3", "A4", "A5", "A6"))

# Loop df columns and plot columns to the figure
for col_name in ['a0','a2','a3','a4','a5','a6']:
    fig.add_trace(go.Scatter(x=df['time'], y=df[col_name],
                        mode='lines', # 'lines' or 'markers'
                        name=col_name))

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
