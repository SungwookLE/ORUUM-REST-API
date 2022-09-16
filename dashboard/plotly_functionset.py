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


def get_stockpricehistory_plotly_object_as_line(ticker):
    """
    This function plots plotly plot
    """

    #get data from db
    stockpricehistory_queryset = StockPriceHistory.objects.filter(
        ticker=ticker)
    result_dict = pd.DataFrame.from_records(
        stockpricehistory_queryset.values())

    #Create graph object Figure object with data
    fig = px.line(result_dict, x='update_date', y='price_close', markers=True)

    #Update layout for graph object Figure
    fig.update_layout(title=ticker,
                      xaxis_title='Date',
                      yaxis_title='Close')

    #Turn graph object into local plotly graph
    fig_plotly_object = plot({'data': fig}, output_type='div')

    return fig_plotly_object


def get_stocklist_plotly_object_as_bar(market):
    """
    This function plots plotly plot
    """
    #get data from db
    stocklist_queryset = StockList.objects.filter(market__icontains=market)
    result_dict = pd.DataFrame.from_records(
        stocklist_queryset.values())

    #Create graph object Figure object with data
    fig = px.bar(result_dict, x='ticker', y='price')

    #Update layout for graph object Figure
    fig.update_layout(title=market + ": " + result_dict['update_date'][0].strftime("%Y.%m.%d"),
                      xaxis_title='ticker',
                      yaxis_title='price')

    #Turn graph object into local plotly graph
    fig_plotly_object = plot({'data': fig}, output_type='div')

    return fig_plotly_object


#########################################################################
# for stateless-dash-app
#########################################################################
# GET data from database
ticker_from_stocklist = StockPriceHistory.objects.values_list('ticker')
ticker_from_stocklist = set(ticker_from_stocklist)
ticker_dropdown_options = [ticker[0] for ticker in ticker_from_stocklist]

# Create DjangoDash applicaiton
app = DjangoDash(name='StockPriceHistory')

# Configure app layout
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
                 style={"backgroundColor": "#FFF0F5"})])
])
##########################################################################


@app.callback(Output('history_plot', 'figure'),  # id of html component
             [Input('ticker_options', 'value')])  # id of html component
def callback_stockpricehistory_as_line(ticker):
    """
    This function creates dash app for plotting variable stats
    Output: Figure object
    """
    #Get table from SQL result
    stockpricehistory_queryset = StockPriceHistory.objects.filter(
        ticker=ticker)
    dash_plot_table = pd.DataFrame.from_records(
        stockpricehistory_queryset.values())
    fig = go.Figure()
    #Create graph object Figure object with data
    fig.add_trace(go.Scatter(
        x=dash_plot_table["update_date"], y=dash_plot_table["price_close"], mode='lines+markers'))

    #Update layout for graph object Figure
    fig.update_layout(title=ticker,
                      xaxis_title='Date',
                      yaxis_title='Close')
    return fig
