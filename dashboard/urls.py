#  file: dashboard/urls.py


from django.urls import path, include
from dashboard.views import dash_stock_as_line_view, plotly_stock_as_line_view, plotly_stocks_all_as_bar_view

app_name = 'dashboard'

urlpatterns = [
    path('line/<str:ticker>/', plotly_stock_as_line_view, name="plot-stock"),
    path('bar/<str:market>/', plotly_stocks_all_as_bar_view, name="bar-stocks"),
    path('dash/', dash_stock_as_line_view, name="dash-stock"),
]
