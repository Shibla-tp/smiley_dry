# Generated by Django 4.2.4 on 2023-08-18 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smile_dryApp', '0050_alter_laundry_vendor_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laundry',
            name='vendor_details',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
