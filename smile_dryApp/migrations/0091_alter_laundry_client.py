# Generated by Django 4.2.4 on 2023-09-07 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smile_dryApp', '0090_alter_laundry_vendor_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laundry',
            name='client',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='client_user', to='smile_dryApp.customer'),
        ),
    ]
