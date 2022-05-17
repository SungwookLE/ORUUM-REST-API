from django.contrib.auth.models import AbstractUser
from django.db import models
from api.models import Stock_List


class User_List(AbstractUser):
    """유저의 회원가입 정보
    pk = "id"
    columns = ["email", "first_name", "last_name", "update_dt", "create_dt"]
    Create a custom user model by inheriting AbstractUser ...
    """
    id = models.BigAutoField(help_text="id_user_list", primary_key=True)
    update_dt = models.DateTimeField(verbose_name='update_dt', auto_now=True)
    create_dt = models.DateTimeField(
        verbose_name='create_dt', auto_now_add=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    # 회원 가입 시 아래 항목 입력을 필수로 지정
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    class Meta:
        verbose_name_plural = "User_lists"

    def __str__(self):
        return str(self.email)


class User_Interest(models.Model):
    """유저의 관심종목
    pk = "id"
    columns = ["id", "id_user", "ticker", "update_dt", "create_dt"]
    """
    id = models.BigAutoField(help_text="id_user_interest", primary_key=True)

    id_user = models.ForeignKey(
        User_List, related_name="user_interest", on_delete=models.CASCADE, db_column="id_user")
    ticker = models.ForeignKey(
        Stock_List, related_name="user_interest", on_delete=models.CASCADE, db_column="ticker")

    update_dt = models.DateTimeField(verbose_name='update_dt', auto_now=True)
    create_dt = models.DateTimeField(
        verbose_name='create_dt', auto_now_add=True)

    def __str__(self):
        return str(self.id)


class User_Portfolio(models.Model):
    """유저의 포트폴리오
    pk = "id"
    columns = ["id", "id_user", "ticker", "number_stock", "average_price","price_earning_ratio", "price_return_won", "price_return_dollar","update_dt", "create_dt"]
    """
    id = models.BigAutoField(help_text="id_user_portfolio", primary_key=True)
    id_user = models.ForeignKey(
        User_List, related_name="user_portfolio", on_delete=models.CASCADE, db_column="id_user")
    ticker = models.ForeignKey(
        Stock_List, related_name="user_portfolio", on_delete=models.CASCADE, db_column="ticker")

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
