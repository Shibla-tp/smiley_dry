# Generated by Django 4.2.4 on 2023-09-06 16:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smile_dryApp', '0087_alter_laundry_franchise_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laundry',
            name='franchise_details',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='franchise_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='laundry',
            name='vendor_details',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='vendor_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
