from django import forms
from django.utils.translation import gettext_lazy as _

from .models import User_List


from django.contrib.auth import get_user_model


class SignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']

    def save(self, user):
        user.save()
