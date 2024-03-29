#  file: accounts/admin.py

from django.contrib import admin
from accounts.models import UserList, UserInterest, UserPortfolio, UserWallet
from django.contrib.auth.admin import UserAdmin


@admin.register(UserList)
class UserListAdmin(UserAdmin):
    list_display = [ 'id_user', 'is_staff', 'username', 'email','last_login']


@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    search_fields = ['ticker']


@admin.register(UserPortfolio)
class UserPortfolioAdmin(admin.ModelAdmin):
    search_fields = ['ticker']

@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    pass