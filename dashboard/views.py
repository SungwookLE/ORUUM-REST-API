#  file: dashboard/views.py

from django.shortcuts import render
from rest_framework.decorators import api_view
from .plotly_set import plot_plotly


# Create your views here.
@api_view(['GET'])
def plotly_page(request, ticker):
    if request.method == 'GET':
        #Plotly visualizations
        target_plot = plot_plotly(ticker)
        context = {'target_plot': target_plot, "ticker": ticker}
        return render(request, "dashboard/static_dash_template.html", context=context)


@api_view(['GET'])
def dash_page(request):
    if request.method == 'GET':
        return render(request, "dashboard/interactive_dash_template.html")
