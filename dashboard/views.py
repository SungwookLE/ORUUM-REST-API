#  file: dashboard/views.py
from django.shortcuts import render
from dashboard.plotly_functionset import get_stockpricehistory_plotly_object_as_line \
                                         , get_stocklist_plotly_object_as_bar


# Create your views here.
def stockpricehistory_as_line_view(request, ticker):
    if request.method == 'GET':
        #Plotly visualizations
        target_plot = get_stockpricehistory_plotly_object_as_line(ticker)
        context = {'target_plot': target_plot}
        return render(request, "dashboard/plotly_stock.html", context=context)


def stocklist_as_bar_view(request, market):
    if request.method == 'GET':
        #Plotly visualizations
        target_plot = get_stocklist_plotly_object_as_bar(market)
        context = {'target_plot': target_plot}
        return render(request, "dashboard/plotly_stock.html", context=context)


def stockpricehistory_dash_as_line_view(request):
    if request.method == 'GET':
        return render(request, "dashboard/dash_stock.html")