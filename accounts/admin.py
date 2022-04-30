from django.contrib import admin
from accounts.models import User_List, User_Interest, User_Portfolio
from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(User_List)
class UserListAdmin(admin.ModelAdmin):
    pass

@admin.register(User_Interest)
class UserInterestAdmin(admin.ModelAdmin):
    pass

@admin.register(User_Portfolio)
class UserPortfolioAdmin(admin.ModelAdmin):
    pass