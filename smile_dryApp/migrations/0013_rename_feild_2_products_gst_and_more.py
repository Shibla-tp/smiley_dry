# Generated by Django 4.0.4 on 2023-08-04 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smile_dryApp', '0012_rename_productpurchace_productpurchase'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='feild_2',
            new_name='GST',
        ),
        migrations.RenameField(
            model_name='products',
            old_name='feild_3',
            new_name='purchase_rate',
        ),
        migrations.RenameField(
            model_name='products',
            old_name='pincode',
            new_name='sale_price',
        ),
    ]
