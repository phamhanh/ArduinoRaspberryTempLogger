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
import serial, time, sys
import os, errno

app = dash.Dash()
port = 8051
default_csv = "temp.csv"
if len(sys.argv) == 2:
    csv = sys.argv[1]
else:
    csv = default_csv

def open_browser():
	webbrowser.open_new("http://localhost:{}".format(port))

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

#Create a dash app layout with figure, fig_done and fig_average
app.layout = html.Div([
    dcc.Graph(id='live-graph-tempeh'),
    dcc.Graph(id='live-graph-room'),
    dcc.Graph(id='live-graph-air'),
    dcc.Graph(id='live-graph-heat'),
    dcc.Graph(id='live-graph-done'),
    #dcc.Graph(id='live-graph-average'),
    #dcc.Graph(id='live-graph-sum'),
    dcc.Graph(id='live-graph-heat_sum'),
    dcc.Interval(
            id='graph-update',
            interval=60*1000, # in milliseconds
            n_intervals=0
        )
])

#Create a function to update live-graph
@app.callback( [Output('live-graph-tempeh', 'figure'),
                Output('live-graph-room', 'figure'),
                Output('live-graph-air', 'figure'),
                Output('live-graph-heat', 'figure'),
                Output('live-graph-done', 'figure'),
                #Output('live-graph-average', 'figure'),
                #Output('live-graph-sum', 'figure'),
                Output('live-graph-heat_sum', 'figure')],
                [Input('graph-update', 'n_intervals')])
#Create a function to update graph
def update_graph_scatter(n):
    df = pd.read_csv(csv)
    #convert all colums to numeric
    df['time'] = pd.to_datetime(df['time'],unit='m')

    df = df[['time', '55', '68', '57', '64', '56', '58', '59', '60', '61', '66', '62', '67', '54', '63', '69', '65']]

    # Air around tempeh
    df = df.rename(columns={'55': 'TL A1 Air Top Left Back'})
    df = df.rename(columns={'68': 'TL A14 Air Top Left Front'})
    df = df.rename(columns={'57': 'MM A3 Air Middle Middle'})
    df = df.rename(columns={'64': 'BR A10 Air Bottom Right Front'})

    # Air in room
    df = df.rename(columns={'56': 'A2 Room Behind Cooler'})
    df = df.rename(columns={'58': 'A4 Room Middle Middle'})
    df = df.rename(columns={'59': 'A5 Room Cooler'})
    df = df.rename(columns={'60': 'A6 Room Top'})
    df = df.rename(columns={'61': 'A7 Room Heater'})

    # Tempeh
    df = df.rename(columns={'66': 'TL A12 Tempeh Top Left'})
    df = df.rename(columns={'62': 'TR A8 Tempeh Top Right'})
    df = df.rename(columns={'67': 'ML A13 Tempeh Middle Left'})
    df = df.rename(columns={'54': 'MM A0 Tempeh Sensor Middle Middle'})
    df = df.rename(columns={'63': 'MR A9 Tempeh Middle Right'})
    df = df.rename(columns={'69': 'BL A15 Tempeh Bottom Left'})
    df = df.rename(columns={'65': 'BR A11 Tempeh Bottom Right'})

    #Faulty sensor, remove column A6 Room Top from df
    df = df.drop(columns=['A6 Room Top'])

    #Faulty sensor, remove column A14 Top Left Front from df
    df = df.drop(columns=['TL A14 Air Top Left Front'])


    #Create a figure
    fig_air = go.Figure()

    #for each column in df add a trace to the figure
    for column in df:
        #if column does not have Tempeh or Room in name
        if 'Tempeh' not in column and 'Room' not in column:
            #If not time in column
            if column != 'time':
                #add a trace to the figure
                fig_air.add_trace(go.Scatter(x = df['time'], y = df[column], name=column, line_shape='spline',line_smoothing=1.3))
    #Sort by column name by using category_orders
    fig_air.update_layout(legend={'traceorder':'normal'})
            
        


    #Repeat for fig_tempeh when column has Tempeh in name
    fig_tempeh = go.Figure()
    for column in df:
        if 'Tempeh' in column:
            fig_tempeh.add_trace(go.Scatter(x = df['time'], y = df[column], name=column, line_shape='spline',line_smoothing=1.3))
    fig_tempeh.update_layout(legend={'traceorder':'normal'})

    
    #Repeat for fig_room when column has Room in name
    fig_room = go.Figure()
    for column in df:
        if 'Room' in column:
            fig_room.add_trace(go.Scatter(x = df['time'], y = df[column], name=column, line_shape='spline',line_smoothing=1.3))
    fig_room.update_layout(legend={'traceorder':'normal'})

    #Convert all columns to numeric
    df = df.apply(pd.to_numeric, errors='ignore')
    #loop over every column and set a variable air_top, air_bottom, air_middle if column has air and top, bottom or middle in name
    for column in df:
        if 'Air' in column:
            if 'Top' in column:
                air_top = column
            if 'Bottom' in column:
                air_bottom = column
            if 'Middle' in column:
                air_middle = column

    #loop over every column and if column has tempeh in name and has top, bottom or middle in name then subtract the air_top, air_bottom or air_middle from the column and add a column to df that is the result
    for column in df:
        if 'Tempeh' in column:
            if 'Top' in column:
                df[column + ' - Heat'] = df[column] - df[air_top]
            if 'Bottom' in column:
                df[column + ' - Heat'] = df[column] - df[air_bottom]
            if 'Middle' in column:
                df[column + ' - Heat'] = df[column] - df[air_middle]
    #Create scatter graph with time on x axis and the column with - Heat in the name on the y axis
    fig_heat = go.Figure()
    for column in df:
        if '- Heat' in column:
            fig_heat.add_trace(go.Scatter(x = df['time'], y = df[column], name=column, line_shape='spline',line_smoothing=1.3))
    fig_heat.update_layout(legend={'traceorder':'normal'})

            

    #loop over every  column in df 
    for column in df:
        #if column is not time
        if column != 'time':
            #convert column to numeric
            df[column + 'sum'] = df[column].sum(numeric_only=True)

    #loop over every column in df with sum in the name
    for column in df.filter(regex='sum'):
        #create new column in df that is the column divided by 72000 times 100. 72.000 is 48 hours of 25C (25 * 48 * 60)
        df[column + ' % Done' ] = df[column] / 72000 * 100
    #Find all colums with % in the name and rename to remove sum
    df = df.rename(columns=lambda x: x.replace('sum % Done', ' % Done'))

    df_last = df.tail(1)
    print_full(df_last.filter(regex='Done'))
    x_done=[]
    y_done=[]

    #Loop over every column in df with Done and Tempeh in name
    for column in df_last.filter(regex='Tempeh'):
        #Has Done in the name
        if 'Done' in column and not 'Heat' in column:
            #add column name to x
            x_done.append(column)
            #Add column value to y
            y_done.append(df_last[column].values[0])
    fig_done = go.Figure(go.Bar(x=x_done, 
                                y=y_done, 
                                marker_color='rgb(158,202,225)', 
                                marker_line_color='rgb(8,48,107)', 
                                marker_line_width=1.5, 
                                opacity=0.6))


    #create x_heat, y_heat and calculate sum of df for columns with heat in name, create a bar graph with x_heat and y_heat
    x_heat=[]
    y_heat=[]
    for column in df_last.filter(regex='Tempeh'):
        if 'Heatsum' in column :
            x_heat.append(column)
            y_heat.append(df[column].sum())
    fig_heat_sum = go.Figure(go.Bar(x=x_heat, y=y_heat))

    #Return the figure
    return fig_tempeh, fig_room, fig_air, fig_heat, fig_done, fig_heat_sum

    



if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run_server(debug=True, use_reloader=True, host='0.0.0.0', port=port) 
