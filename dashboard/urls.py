from django.urls import path, include
from dashboard.views import dash_page

app_name='dashboard'
urlpatterns = [
    path('', dash_page, name ="my_dash"),
]
