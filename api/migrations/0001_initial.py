# Generated by Django 4.0 on 2022-04-30 14:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock_List',
            fields=[
                ('ticker', models.CharField(help_text='Ticker(Symbol)', max_length=20, primary_key=True, serialize=False)),
                ('update_date', models.DateField(default=datetime.datetime.today, help_text='업데이트 날짜')),
                ('name_english', models.CharField(default='', help_text='주식명(영어)', max_length=50)),
                ('name_korea', models.CharField(blank=True, help_text='주식명(한국어)', max_length=50, null=True)),
                ('market', models.CharField(default='', help_text='상장사', max_length=20)),
                ('price', models.FloatField(default=0, help_text='주가')),
                ('price_open', models.FloatField(default=0, help_text='시가')),
                ('prevclose', models.FloatField(default=0, help_text='전일가')),
                ('price_high', models.FloatField(default=0, help_text='고가')),
                ('price_low', models.FloatField(default=0, help_text='저가')),
                ('volume', models.FloatField(default=0, help_text='거래량')),
                ('update_dt', models.DateTimeField(auto_now=True, verbose_name='update_dt')),
                ('create_dt', models.DateTimeField(auto_now_add=True, verbose_name='create_dt')),
            ],
            options={
                'ordering': ['ticker'],
            },
        ),
        migrations.CreateModel(
            name='Stock_Price_History',
            fields=[
                ('id', models.BigAutoField(help_text='id_stock_price_history', primary_key=True, serialize=False)),
                ('update_date', models.DateField(default=datetime.datetime.today, help_text='날짜')),
                ('price_open', models.FloatField(blank=True, help_text='시가', null=True)),
                ('price_high', models.FloatField(default=0, help_text='고가')),
                ('price_low', models.FloatField(default=0, help_text='저가')),
                ('price_close', models.FloatField(blank=True, help_text='종가', null=True)),
                ('adj_close', models.FloatField(blank=True, help_text='조정 종가', null=True)),
                ('volume', models.FloatField(default=0, help_text='거래량')),
                ('splits', models.FloatField(blank=True, help_text='주식분할 내역', null=True)),
                ('dividends', models.FloatField(blank=True, help_text='배당 내역', null=True)),
                ('update_dt', models.DateTimeField(auto_now=True, verbose_name='update_dt')),
                ('create_dt', models.DateTimeField(auto_now_add=True, verbose_name='create_dt')),
                ('ticker', models.ForeignKey(db_column='ticker', on_delete=django.db.models.deletion.CASCADE, related_name='stock_price_history', to='api.stock_list')),
            ],
            options={
                'ordering': ['-update_date', 'ticker'],
            },
        ),
        migrations.CreateModel(
            name='Stock_Information_History',
            fields=[
                ('id', models.BigAutoField(help_text='id_stock_information_history', primary_key=True, serialize=False)),
                ('update_date', models.DateField(default=datetime.datetime.today, help_text='업데이트 날짜', verbose_name='date')),
                ('total_assets', models.FloatField(blank=True, help_text='자산총계', null=True)),
                ('curruent_assets', models.FloatField(blank=True, help_text='유동자산', null=True)),
                ('inventory', models.FloatField(blank=True, help_text='재고자산', null=True)),
                ('quick_assets', models.FloatField(blank=True, help_text='당좌자산', null=True)),
                ('non_current_assets', models.FloatField(blank=True, help_text='비유동자산', null=True)),
                ('investments', models.FloatField(blank=True, help_text='투자자산', null=True)),
                ('tagible_assets', models.FloatField(blank=True, help_text='유형자산', null=True)),
                ('liabilities', models.FloatField(blank=True, help_text='부채', null=True)),
                ('current_liabilities', models.FloatField(blank=True, help_text='유동부채', null=True)),
                ('non_current_liabilities', models.FloatField(blank=True, help_text='비유동부채', null=True)),
                ('total_assets_ratio', models.FloatField(blank=True, help_text='유동비율', null=True)),
                ('quick_assets_ratio', models.FloatField(blank=True, help_text='당좌비율', null=True)),
                ('liabilities_ratio', models.FloatField(blank=True, help_text='부채비율', null=True)),
                ('total_revenue', models.FloatField(blank=True, help_text='매출액', null=True)),
                ('gross_profit', models.FloatField(blank=True, help_text='매출총이익', null=True)),
                ('operating_income', models.FloatField(blank=True, help_text='영업이익', null=True)),
                ('net_income', models.FloatField(blank=True, help_text='순이익', null=True)),
                ('total_revenue_ratio', models.FloatField(blank=True, help_text='매출이익률', null=True)),
                ('operating_income_ratio', models.FloatField(blank=True, help_text='영업이익률', null=True)),
                ('net_income_ratio', models.FloatField(blank=True, help_text='순이익률', null=True)),
                ('operating_cash_flow', models.FloatField(blank=True, help_text='영업현금흐름', null=True)),
                ('update_dt', models.DateTimeField(auto_now=True, verbose_name='update_dt')),
                ('create_dt', models.DateTimeField(auto_now_add=True, verbose_name='create_dt')),
                ('ticker', models.ForeignKey(db_column='ticker', on_delete=django.db.models.deletion.CASCADE, related_name='stock_information_history', to='api.stock_list')),
            ],
            options={
                'ordering': ['-update_date', 'ticker'],
            },
        ),
    ]
