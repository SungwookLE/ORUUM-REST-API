# Generated by Django 4.0 on 2022-04-05 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_stockinformation_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockinformation',
            name='symbol',
            field=models.OneToOneField(db_column='symbol', on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='api.stockprice'),
        ),
    ]
