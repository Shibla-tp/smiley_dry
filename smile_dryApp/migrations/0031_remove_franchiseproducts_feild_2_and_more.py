# Generated by Django 4.2.4 on 2023-08-11 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smile_dryApp', '0030_alter_coupon_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='franchiseproducts',
            name='feild_2',
        ),
        migrations.AddField(
            model_name='franchiseproducts',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='Products'),
        ),
    ]
