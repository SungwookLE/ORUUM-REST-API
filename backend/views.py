#  file: backend/views.py
from datetime import datetime
from django.views.generic import TemplateView
from api.models import StockList
from django.shortcuts import get_object_or_404

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        """ get_context_data let you fill the template context """
        context = super(HomeView, self).get_context_data(**kwargs)
        # Get Related publishers
        #obj = get_object_or_404(StockList.objects.only('update_date'), ticker="AAPL")
        #context['last_update'] = obj.update_date.strftime("%Y.%m.%d")
        return context