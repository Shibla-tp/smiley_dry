# Generated by Django 4.2.4 on 2023-09-02 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smile_dryApp', '0072_alter_laundry_pickup_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffs',
            name='aadhar',
            field=models.FileField(blank=True, null=True, upload_to='Staff_details'),
        ),
        migrations.AddField(
            model_name='staffs',
            name='pan_card',
            field=models.FileField(blank=True, null=True, upload_to='Staff_details'),
        ),
        migrations.AddField(
            model_name='staffs',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='Staff_details'),
        ),
    ]
