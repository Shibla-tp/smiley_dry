# Generated by Django 4.2.4 on 2023-09-05 04:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smile_dryApp', '0080_alter_coupon_franchise_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='franchise_details',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL),
        ),
    ]