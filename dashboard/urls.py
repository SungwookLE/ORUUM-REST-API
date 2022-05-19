#  file: dashboard/urls.py


from django.urls import path, include
from dashboard.views import dash_page, plotly_page

app_name='dashboard'

urlpatterns = [
    path('plotly/', plotly_page, name ="my_plotly"),
    path('dash/', dash_page, name ="my_dash"),
]
