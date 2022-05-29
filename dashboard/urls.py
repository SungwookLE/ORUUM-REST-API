#  file: dashboard/urls.py


from django.urls import path, include
from dashboard.views import stockpricehistory_as_line_view, stocklist_as_bar_view, stockpricehistory_dash_as_line_view

app_name = 'dashboard'

urlpatterns = [
    path('line/<str:ticker>/', stockpricehistory_as_line_view, name="plot-stock"),
    path('bar/<str:market>/', stocklist_as_bar_view, name="bar-stocks"),
    path('dash/', stockpricehistory_dash_as_line_view, name="dash-stock"),
]
