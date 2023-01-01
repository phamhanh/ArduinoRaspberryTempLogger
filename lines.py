import pandas as pd
import plotly.graph_objects as go # or plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import webbrowser
from threading import Timer

app = dash.Dash()
port = 8050

def open_browser():
	webbrowser.open_new("http://localhost:{}".format(port))

app.layout = html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(
            id='graph-update',
            interval=60*1000, # in milliseconds
            n_intervals=0
        )
])

@app.callback(
    Output('live-graph', 'figure'),
    [ Input('graph-update', 'n_intervals') ]
)
def update_graph_scatter(n):
    df = pd.read_csv('temp.csv')
    df['time'] = pd.to_datetime(df['time'],unit='m')

    fig = go.Figure(go.Scatter(x = df['time'], y = df['54'], name='0TM Tempeh Middle'))
    fig.add_trace(go.Scatter(x = df['time'], y = df['55'], name='1ATLB Top Left Back'))
    fig.add_trace(go.Scatter(x = df['time'], y = df['56'], name='?2ATMF Behind Fridge')) 
    fig.add_trace(go.Scatter(x = df['time'], y = df['57'], name='3ATMM Middle Middle'))
    fig.add_trace(go.Scatter(x = df['time'], y = df['64'], name='10ARB Right Bottom'))
    #fig.add_trace(go.Scatter(x = df['time'], y = df['60'], name='?6 Top Room')) 
    fig.add_trace(go.Scatter(x = df['time'], y = df['58'], name='4A-Middle Room'))
    #fig.add_trace(go.Scatter(x = df['time'], y = df['68'], name='?14ATL Top Left Front'))
    fig.add_trace(go.Scatter(x = df['time'], y = df['59'], name='5A Fridge'))
    fig.add_trace(go.Scatter(x = df['time'], y = df['61'], name='7 Heater')) 
    fig.add_trace(go.Scatter(x = df['time'], y = df['62'], name='A8 Tempeh Top Right'))
    fig.add_trace(go.Scatter(x = df['time'], y = df['66'], name='A12 Tempeh Top Left'))
    fig.add_trace(go.Scatter(x = df['time'], y = df['63'], name='A9 Tempeh Middle Right'))
    fig.add_trace(go.Scatter(x = df['time'], y = df['67'], name='a13 Tempeh Middle Left'))
    fig.add_trace(go.Scatter(x = df['time'], y = df['65'], name='A11 Tempeh Bottom Right'))
    fig.add_trace(go.Scatter(x = df['time'], y = df['69'], name='A15 Tempeh Bottom Left'))

    fig.update_layout(  plot_bgcolor='rgb(230, 230,230)',
                        margin=dict(l=1, r=1, t=1, b=1),
                        uirevision=True,
                        showlegend=True)

    fig.update_layout(yaxis=dict(range=[5,30]))
    
    fig.update_xaxes(
        tickformat="%-H:%M\nDay %e",
    )
    return fig

if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run_server(debug=True, use_reloader=True, host='0.0.0.0') 
