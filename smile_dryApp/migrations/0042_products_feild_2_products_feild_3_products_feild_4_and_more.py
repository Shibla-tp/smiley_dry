# Generated by Django 4.2.4 on 2023-08-12 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smile_dryApp', '0041_rename_final_price_products_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='feild_2',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='products',
            name='feild_3',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='products',
            name='feild_4',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='products',
            name='feild_5',
            field=models.CharField(default=0, max_length=100),
        ),
    ]