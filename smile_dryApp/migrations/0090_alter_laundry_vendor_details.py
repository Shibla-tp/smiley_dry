# Generated by Django 4.2.4 on 2023-09-07 04:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smile_dryApp', '0089_alter_laundry_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laundry',
            name='vendor_details',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vendor_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
