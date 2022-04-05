# Generated by Django 4.0 on 2022-04-05 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockPrice',
            fields=[
                ('symbol', models.CharField(default='', max_length=30, primary_key=True, serialize=False, verbose_name='symbol')),
                ('name', models.CharField(default='', max_length=50, verbose_name='name')),
                ('market', models.CharField(default='', max_length=50, verbose_name='market')),
                ('update_dt', models.DateTimeField(auto_now=True, verbose_name='update_dt')),
                ('create_dt', models.DateTimeField(auto_now_add=True, verbose_name='create_dt')),
                ('price', models.FloatField(default=0, verbose_name='price')),
                ('open', models.FloatField(default=0, verbose_name='open')),
                ('prevclose', models.FloatField(default=0, verbose_name='prevclose')),
                ('high', models.FloatField(default=0, verbose_name='high')),
                ('low', models.FloatField(default=0, verbose_name='low')),
                ('volume', models.FloatField(default=0, verbose_name='volume')),
            ],
        ),
        migrations.CreateModel(
            name='StockInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_dt', models.DateTimeField(auto_now=True, verbose_name='update_dt')),
                ('create_dt', models.DateTimeField(auto_now_add=True, verbose_name='create_dt')),
                ('total_assets', models.FloatField(default=0, help_text='자산총계', verbose_name='total_assets')),
                ('curruent_assets', models.FloatField(default=0, help_text='유동자산', verbose_name='curruent_assets')),
                ('inventory', models.FloatField(default=0, help_text='재고자산', verbose_name='inventory')),
                ('quick_assets', models.FloatField(default=0, help_text='당좌자산', verbose_name='quick_assets')),
                ('non_current_assets', models.FloatField(default=0, help_text='비유동자산', verbose_name='non_current_assets')),
                ('investments', models.FloatField(default=0, help_text='투자자산', verbose_name='investments')),
                ('tagible_assets', models.FloatField(default=0, help_text='유형자산', verbose_name='tagible_assets')),
                ('liabilities', models.FloatField(default=0, help_text='부채', verbose_name='liabilities')),
                ('current_liabilities', models.FloatField(default=0, help_text='유동부채', verbose_name='current_liabilities')),
                ('non_current_liabilities', models.FloatField(default=0, help_text='비유동부채', verbose_name='non_current_liabilities')),
                ('total_assets_ratio', models.FloatField(default=0, help_text='유동비율', verbose_name='total_assets_ratio')),
                ('quick_assets_ratio', models.FloatField(default=0, help_text='당좌비율', verbose_name='quick_assets_ratio')),
                ('liabilities_ratio', models.FloatField(default=0, help_text='부채비율', verbose_name='liabilities_ratio')),
                ('total_revenue', models.FloatField(default=0, help_text='매출액', verbose_name='total_revenue')),
                ('gross_profit', models.FloatField(default=0, help_text='매출총이익', verbose_name='gross_profit')),
                ('operating_income', models.FloatField(default=0, help_text='영업이익', verbose_name='operating_income')),
                ('net_income', models.FloatField(default=0, help_text='순이익', verbose_name='net_income')),
                ('total_revenue_ratio', models.FloatField(default=0, help_text='매출이익률', verbose_name='total_revenue_ratio')),
                ('operating_income_ratio', models.FloatField(default=0, help_text='영업이익률', verbose_name='operating_income_ratio')),
                ('net_income_ratio', models.FloatField(default=0, help_text='순이익률', verbose_name='net_income_ratio')),
                ('operating_cash_flow', models.FloatField(default=0, help_text='영업현금흐름', verbose_name='operating_cash_flow')),
                ('symbol', models.ForeignKey(db_column='symbol', on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='api.stockprice')),
            ],
        ),
    ]
