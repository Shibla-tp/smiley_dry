# Generated by Django 4.2.4 on 2023-08-24 07:22

from django.db import migrations, models
import smile_dryApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('smile_dryApp', '0066_laundryproducts_total_amount_cgst_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.IntegerField(blank=True, null=True, unique=True, validators=[smile_dryApp.models.validate_phone]),
        ),
    ]
