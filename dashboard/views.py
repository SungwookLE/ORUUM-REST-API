#  file: dashboard/views.py

from django.shortcuts import render
from dashboard.plotly_functionset import plotly_stock_as_line, plotly_stocks_all_as_bar


# Create your views here.
def plotly_stock_as_line_view(request, ticker):
    if request.method == 'GET':
        #Plotly visualizations
        target_plot = plotly_stock_as_line(ticker)
        context = {'target_plot': target_plot}
        return render(request, "dashboard/plotly_stock.html", context=context)


def plotly_stocks_all_as_bar_view(request, market):
    if request.method == 'GET':
        #Plotly visualizations
        target_plot = plotly_stocks_all_as_bar(market)
        context = {'target_plot': target_plot}
        return render(request, "dashboard/plotly_stock.html", context=context)


def dash_stock_as_line_view(request):
    if request.method == 'GET':
        return render(request, "dashboard/dash_stock.html")