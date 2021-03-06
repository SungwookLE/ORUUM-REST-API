#  file: accounts/forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from accounts.models import UserList

from django.utils.translation import gettext_lazy as _


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        # 소셜 auth를 이용한 회원가입의 경우, 비밀번호 요청 X
        del self.fields['password1']
        del self.fields['password2']

        self.fields['username'].disabled = True
        self.fields['email'].disabled = True

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name"]

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
