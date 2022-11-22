#  file: accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from api.models import StockList


class UserList(AbstractUser):
    """유저의 회원가입 정보
    pk is "id"
    columns are ["email", "username", "update_dt", "create_dt"]
    Create a custom user model by inheriting AbstractUser ...
    """
    id = models.BigAutoField(help_text="id_userlist", primary_key=True)
    email = models.EmailField(unique=True)
    thumbnail_image = models.CharField(blank=True, null=True, help_text ="프로필 이미지 URL", max_length=200)
    kakao_access_token= models.CharField(blank=True, null=True, max_length=200)

    # 회원 가입 시 아래 항목 입력을 필수로 지정
    # REQUIRED_FIELDS = ["email"]

    update_dt = models.DateTimeField(verbose_name='update_dt', auto_now=True)
    create_dt = models.DateTimeField(
        verbose_name='create_dt', auto_now_add=True)

    class Meta:
        verbose_name_plural = "User lists"

    def __str__(self):
        return str(self.email)


class UserInterest(models.Model):
    """유저의 관심종목
    pk is "id"
    columns are ["id", "id_user", "ticker", "update_dt", "create_dt"]
    """
    id = models.BigAutoField(help_text="id_userinterest", primary_key=True)
    id_user = models.ForeignKey(
        UserList, related_name="userinterest", on_delete=models.CASCADE, db_column="id_user")
    ticker = models.ForeignKey(
        StockList, related_name="userinterest", on_delete=models.CASCADE, db_column="ticker")

    update_dt = models.DateTimeField(verbose_name='update_dt', auto_now=True)
    create_dt = models.DateTimeField(
        verbose_name='create_dt', auto_now_add=True)

    def __str__(self):
        return str(self.id)


class UserPortfolio(models.Model):
    """유저의 포트폴리오
    pk is "id"
    columns are ["id", "id_user", "ticker", "number_stock", "average_price","price_earning_ratio", "price_return_won", "price_return_dollar","update_dt", "create_dt"]
    """
    id = models.BigAutoField(help_text="id_userportfolio", primary_key=True)
    id_user = models.ForeignKey(
        UserList, related_name="userportfolio", on_delete=models.CASCADE, db_column="id_user")
    ticker = models.ForeignKey(
        StockList, related_name="userportfolio", on_delete=models.CASCADE, db_column="ticker")

    number_stock = models.IntegerField(blank=True, null=True, help_text='보유수량')
    average_price = models.FloatField(blank=True, null=True, help_text='평균매입가')
    price_earning_ratio = models.FloatField(
        blank=True, null=True, help_text='주가수익률')
    price_return_won = models.FloatField(
        blank=True, null=True, help_text='수익금(원)')
    price_return_dollar = models.FloatField(
        blank=True, null=True, help_text='수익금(달러)')

    update_dt = models.DateTimeField(verbose_name='update_dt', auto_now=True)
    create_dt = models.DateTimeField(
        verbose_name='create_dt', auto_now_add=True)

    def __str__(self):
        return str(self.id)


class UserWallet(models.Model):
    id_user = models.OneToOneField(UserList, related_name="userwallet", on_delete=models.CASCADE, db_column="id_user", primary_key=True)
    deposit = models.FloatField(help_text="deposit dollar", blank=True, null=True, default=0)

    update_dt = models.DateTimeField(verbose_name='update_dt', auto_now=True)
    create_dt = models.DateTimeField(
        verbose_name='create_dt', auto_now_add=True)

    def __str__(self):
        return str(self.id_user)