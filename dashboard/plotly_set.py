#  file: dashboard/plotly_set.py

import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from api.models import StockPriceHistory, StockList
import plotly.express as px

def plot_plotly(ticker):
    """
    This function plots plotly plot
    """

    #get data from db
    stockpricehistory_queryset = StockPriceHistory.objects.filter(
        ticker=ticker)
    result_dict = pd.DataFrame.from_records(
        stockpricehistory_queryset.values())

    #Create graph object Figure object with data
    fig = px.line(
        result_dict, x=result_dict['update_date'], y=result_dict['price_close'])

    #Update layout for graph object Figure
    fig.update_layout(title_text=ticker,
                      xaxis_title='Date',
                      yaxis_title='Close')

    #Turn graph object into local plotly graph
    plotly_plot_obj = plot({'data': fig}, output_type='div')

    return plotly_plot_obj


def dash_plotly(ticker):
    """
    This function creates dash app for plotting variable stats by city selected
    Input: Mysql connection and city specified
    Output: Figure object
    """

    #Get table from SQL result
    stockpricehistory_queryset = StockPriceHistory.objects.filter(
        ticker=ticker)
    dash_plot_table = pd.DataFrame.from_records(
        stockpricehistory_queryset.values())

    #Create graph object Figure object with data
    fig = go.Figure(data=go.Scatter(name='ORUUM',
                    x=dash_plot_table['update_date'], y=dash_plot_table['price_close']))

    #Update layout for graph object Figure
    fig.update_layout(title_text=ticker,
                      xaxis_title='Date',
                      yaxis_title='Close')

    return fig


#GET data from database defaultly
ticker_from_stocklist = StockPriceHistory.objects.values_list('ticker')
ticker_from_stocklist = set(ticker_from_stocklist)
ticker_dropdown_options = [ticker[0] for ticker in ticker_from_stocklist]

#Create DjangoDash applicaiton
app = DjangoDash(name='StockPriceHistory')

#Configure app layout
app.layout = html.Div([
    html.Div([
        #Add dropdown for option selection
        dcc.Dropdown(
                      id='ticker_options',
                      options=[{'label': i, 'value': i}
                               for i in ticker_dropdown_options],
                      value='AAPL')],  # Initial value for the dropdown
             style={'width': '25%', 'margin': '0px auto'}),

    html.Div([
        dcc.Graph(id='history_plot',
                  animate=True,
                  style={"backgroundColor": "#FFF0F5"})])
])


@app.callback(Output('history_plot', 'figure'),  # id of html component
              [Input('ticker_options', 'value')])  # id of html component
def display_value(ticker):
    """
    This function returns figure object according to value input
    Input: Value specified
    Output: Figure object
    """
    #Get city plot with input value
    fig = dash_plotly(ticker)
    return fig
