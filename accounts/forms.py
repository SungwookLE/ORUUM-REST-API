#  file: accounts/forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# (11/23) 아래 부분은 전부 지워도 됨

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        # 소셜 auth를 이용한 회원가입의 경우, 비밀번호 요청 X
        del self.fields['password1']
        del self.fields['password2']

        self.fields['username'].disabled = False
        self.fields['email'].disabled = True
        # (10/30) ALLAUTH를 이용해서 회원가입을 구현하다 보니까, 폼에 전달되는 파라미터를 내 마음대로 조정이 불가능함. allauth 패키지 찾아보고 수정 필요함
        # (10/30) https://django-allauth.readthedocs.io/en/latest/views.html#signup-account-signup 주소와 같이, allauth의 signup 함수를 오버라이딩해서 구현해주어야 하나?
        # print(kargs)


    class Meta:
        model = get_user_model()
        fields = ["username"]

    def signup(self, request, user):
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.save()
