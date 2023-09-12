# Generated by Django 4.2.4 on 2023-08-22 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smile_dryApp', '0062_delete_rider'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rider',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('location', models.CharField(max_length=100, verbose_name='Location')),
                ('username', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=250)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('password1', models.CharField(max_length=250)),
                ('password2', models.CharField(max_length=250)),
                ('is_rider', models.BooleanField(default=True)),
                ('district', models.CharField(max_length=100)),
                ('rider_city', models.CharField(max_length=100)),
                ('franchise_details', models.CharField(max_length=250)),
                ('vendor_details', models.CharField(max_length=250)),
                ('phone', models.IntegerField(blank=True, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('pincode', models.CharField(max_length=100)),
                ('photo', models.FileField(blank=True, null=True, upload_to='Rider_details')),
                ('aadhar', models.FileField(blank=True, null=True, upload_to='Rider_details')),
                ('license', models.FileField(blank=True, null=True, upload_to='Rider_details')),
                ('feild_5', models.CharField(max_length=100)),
            ],
        ),
    ]
