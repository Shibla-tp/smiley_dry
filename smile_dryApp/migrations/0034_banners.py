# Generated by Django 4.2.4 on 2023-08-11 09:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('smile_dryApp', '0033_remove_prices_feild_2_prices_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_type', models.CharField(max_length=250)),
                ('title', models.CharField(max_length=250)),
                ('offer', models.FloatField(default=0, max_length=15)),
                ('status', models.CharField(choices=[('1', 'Active'), ('2', 'Inactive')], default=1, max_length=2)),
                ('delete_flag', models.IntegerField(default=0)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='Banners')),
                ('mobile_image', models.FileField(blank=True, null=True, upload_to='Categories')),
                ('feild_1', models.CharField(max_length=100)),
                ('feild_2', models.CharField(max_length=100)),
                ('feild_3', models.CharField(max_length=100)),
                ('feild_4', models.CharField(max_length=100)),
                ('feild_5', models.CharField(max_length=100)),
            ],
        ),
    ]
