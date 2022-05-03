from django.shortcuts import render
from rest_framework.decorators import api_view
from .plotly_plot import *
from db_parser.dbModule import Database


# Create your views here.
@api_view(['GET'])
def dash_page(request):
    if request.method == 'GET':
        mysql_connection = Database().db
        #Plotly visualizations
        target_plot = plotly_plot(mysql_connection)
        context = {'target_plot': target_plot}
        return render(request, "test_dashplot.html", context=context)
