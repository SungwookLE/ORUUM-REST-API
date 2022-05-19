#  file: dashboard/views.py

from django.shortcuts import render
from rest_framework.decorators import api_view
from .plotly_set import *
from db_handler.dbModule import Database


# Create your views here.
@api_view(['GET'])
def plotly_page(request):
    if request.method == 'GET':
        mysql_connection = Database().db
        #Plotly visualizations
        target_plot = plot_plotly(mysql_connection)
        context = {'target_plot': target_plot}
        return render(request, "test1_dashplot.html", context=context)


@api_view(['GET'])
def dash_page(request):
    if request.method == 'GET':
        #mysql_connection = Database().db
        #Plotly visualizations
        #target_plot = display_value("AAPL")
        #context = {'target_plot': target_plot}
        return render(request, "test2_dashplot.html")
