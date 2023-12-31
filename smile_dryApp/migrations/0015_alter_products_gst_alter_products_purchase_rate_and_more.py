# Generated by Django 4.0.4 on 2023-08-05 06:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('smile_dryApp', '0014_alter_products_gst_alter_products_purchase_rate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='GST',
            field=models.FloatField(default=0, max_length=100),
        ),
        migrations.AlterField(
            model_name='products',
            name='purchase_rate',
            field=models.FloatField(default=0, max_length=100),
        ),
        migrations.AlterField(
            model_name='products',
            name='sale_price',
            field=models.FloatField(default=0, max_length=100),
        ),
        migrations.CreateModel(
            name='StockInFranchise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('franchise_details', models.CharField(max_length=100)),
                ('feild_2', models.CharField(max_length=100)),
                ('feild_3', models.CharField(max_length=100)),
                ('feild_4', models.CharField(max_length=100)),
                ('feild_5', models.CharField(max_length=100)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smile_dryApp.products')),
            ],
            options={
                'verbose_name_plural': 'List of Stock-In',
            },
        ),
    ]
