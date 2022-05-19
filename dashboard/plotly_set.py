#  file: dashboard/plotly_set.py


import pandas as pd
import pymysql.cursors
from plotly.offline import plot
import plotly.graph_objs as go
from os import name
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash


def plot_plotly(mysql_connection):
    """
    This function plots plotly plot
    """
    #Create SQL command string
    sql = """SELECT * FROM api_stock_list"""

    #Get table from SQL result
    with mysql_connection.cursor() as cursor:
      cursor.execute(sql)
      row = cursor.fetchall()

    result_table = pd.DataFrame(row, columns=["ticker", 'update_date', 'name_english', 'name_korea', 'market', 'price',
                                'price_open', 'prevclose', 'price_high', 'price_low', 'volume', 'update_dt', 'create_dt']).iloc[700:750]

    #Create graph object Figure object with data
    fig = go.Figure(
        data=[go.Scatter(name='ORUUM1', x=result_table['ticker'], y=result_table['prevclose']),
              go.Scatter(name='ORUUM2', x=result_table['ticker'], y=result_table['price_high'])]
    )

    #Update layout for graph object Figure
    fig.update_layout(title_text='ORUUM',
                      xaxis_title='Kind',
                      yaxis_title='Price')

    #Turn graph object into local plotly graph
    plotly_plot_obj = plot({'data': fig}, output_type='div')

    return plotly_plot_obj


def dash_plotly(mysql_connection, update_date):
    """
    This function creates dash app for plotting variable stats by city selected
    Input: Mysql connection and city specified
    Output: Figure object
    """
    #Create SQL command string
    sql = """SELECT * FROM api_stock_list WHERE update_date = '{}'""".format(
        update_date)

    #Get table from SQL result
    with mysql_connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchall()

    dash_plot_table = pd.DataFrame(row)

    #Create graph object Figure object with data
    fig = go.Figure(data=go.Scatter(name='ORUUM' + update_date,
                    x=dash_plot_table['ticker'], y=dash_plot_table['prevclose']))

    #Update layout for graph object Figure
    fig.update_layout(title_text='Variable: ' + update_date,
                      xaxis_title='ticker',
                      yaxis_title='prevclose')
    #barmode='stack',
    return fig


#Create Mysql connection
mysql_connection = pymysql.connect(
    host="127.0.0.1", user='root', password='3102', db='oruum_db', cursorclass=pymysql.cursors.DictCursor)

#Get plot options by running SQL query
update_date_options_sql = "SELECT update_date FROM api_stocklist"

with mysql_connection.cursor() as cursor:
    cursor.execute(update_date_options_sql)
    update_date_options = cursor.fetchall()
update_date_options = [x['update_date'] for x in update_date_options]

#Create DjangoDash applicaiton
app = DjangoDash(name='TickerPlot')

#Configure app layout
app.layout = html.Div([
    html.Div([
        #Add dropdown for option selection
        dcc.Dropdown(
                      id='update_date',
                      options=[{'label': i, 'value': i}
                               for i in update_date_options],
                      value='2022-05-10')],  # Initial value for the dropdown
             style={'width': '10%', 'margin': '0px auto'}),

    html.Div([
        dcc.Graph(id='update_plot',
                  animate=True,
                  style={"backgroundColor": "#FFF0F5"})])
])

#Define app input and output callbacks


@app.callback(Output('update_plot', 'figure'),  # id of html component
              [Input('update_date', 'value')])  # id of html component
def display_value(update_date):
    """
    This function returns figure object according to value input
    Input: Value specified
    Output: Figure object
    """
    #Get city plot with input value
    fig = dash_plotly(mysql_connection, update_date)
    return fig
