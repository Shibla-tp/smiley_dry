# Generated by Django 4.2.4 on 2023-08-12 06:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smile_dryApp', '0040_remove_products_price_products_total_purchase_rate_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='final_price',
            new_name='price',
        ),
    ]