# Generated by Django 4.0.4 on 2023-07-25 16:55

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Is admin')),
                ('is_franchise', models.BooleanField(default=False, verbose_name='Is franchise')),
                ('is_vendor', models.BooleanField(default=False, verbose_name='Is vendor')),
                ('is_rider', models.BooleanField(default=False, verbose_name='Is rider')),
                ('is_customer', models.BooleanField(default=False, verbose_name='Is customer')),
                ('location', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('franchise_city', models.CharField(max_length=100)),
                ('contact_person', models.CharField(max_length=100)),
                ('phone', models.IntegerField(blank=True, null=True, unique=True)),
                ('pincode', models.CharField(max_length=100)),
                ('feild_2', models.CharField(max_length=100)),
                ('feild_3', models.CharField(max_length=100)),
                ('feild_4', models.CharField(max_length=100)),
                ('feild_5', models.CharField(max_length=100)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='B2C',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=20)),
                ('service', models.CharField(choices=[('1', 'Dry Clean'), ('2', 'Wash & Fold'), ('3', 'Wash & Iron'), ('4', 'Premium Laundry'), ('5', 'Shoe Cleaning'), ('6', 'Steam Press'), ('7', 'Starching')], max_length=20)),
                ('delivery_date', models.DateField()),
                ('delivery_time', models.CharField(choices=[('1', '9AM - 10AM'), ('2', '10AM - 11AM'), ('3', '11AM - 12PM'), ('4', '12PM - 1PM'), ('5', '1PM - 2PM'), ('6', '2PM - 3PM'), ('7', '3PM - 4PM'), ('8', '4PM - 5PM'), ('9', '5PM - 6PM'), ('10', '6PM - 7PM'), ('11', '7PM - 8PM'), ('12', '8PM - 9PM')], max_length=100)),
                ('Coupon_code', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=100, verbose_name='Location')),
                ('username', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=250)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('password1', models.CharField(max_length=250)),
                ('password2', models.CharField(max_length=250)),
                ('is_customer', models.BooleanField(default=True)),
                ('district', models.CharField(max_length=100)),
                ('franchise_city', models.CharField(max_length=100)),
                ('contact_person', models.CharField(max_length=100)),
                ('phone', models.IntegerField(blank=True, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('pincode', models.CharField(max_length=100)),
                ('feild_2', models.CharField(max_length=100)),
                ('feild_3', models.CharField(max_length=100)),
                ('feild_4', models.CharField(max_length=100)),
                ('feild_5', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'List of Customers',
            },
        ),
        migrations.CreateModel(
            name='Franchise_User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=250)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('password1', models.CharField(max_length=250)),
                ('password2', models.CharField(max_length=250)),
                ('is_franchise', models.BooleanField(default=True)),
                ('district', models.CharField(max_length=100)),
                ('franchise_city', models.CharField(max_length=100)),
                ('contact_person', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=100)),
                ('feild_2', models.CharField(max_length=100)),
                ('feild_3', models.CharField(max_length=100)),
                ('feild_4', models.CharField(max_length=100)),
                ('feild_5', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Laundry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('client', models.CharField(max_length=250)),
                ('contact', models.CharField(blank=True, max_length=250, null=True)),
                ('total_amount', models.FloatField(max_length=15)),
                ('tendered', models.FloatField(max_length=15)),
                ('status', models.CharField(choices=[('0', 'Pending'), ('1', 'In-progress'), ('2', 'Done'), ('3', 'Picked Up')], default=0, max_length=2)),
                ('payment', models.CharField(choices=[('0', 'Unpaid'), ('1', 'Paid')], default=0, max_length=2)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('is_walkin', models.BooleanField(default=True)),
                ('is_pickup', models.BooleanField(default=True)),
                ('franchise_details', models.CharField(max_length=200)),
                ('pincode', models.IntegerField()),
                ('pickup_date', models.DateField()),
                ('pickup_time', models.CharField(choices=[('1', '9AM - 10AM'), ('2', '10AM - 11AM'), ('3', '11AM - 12PM'), ('4', '12PM - 1PM'), ('5', '1PM - 2PM'), ('6', '2PM - 3PM'), ('7', '3PM - 4PM'), ('8', '4PM - 5PM'), ('9', '5PM - 6PM'), ('10', '6PM - 7PM'), ('11', '7PM - 8PM'), ('12', '8PM - 9PM')], max_length=100)),
                ('delivery_date', models.DateField()),
                ('delivery_time', models.CharField(choices=[('1', '9AM - 10AM'), ('2', '10AM - 11AM'), ('3', '11AM - 12PM'), ('4', '12PM - 1PM'), ('5', '1PM - 2PM'), ('6', '2PM - 3PM'), ('7', '3PM - 4PM'), ('8', '4PM - 5PM'), ('9', '5PM - 6PM'), ('10', '6PM - 7PM'), ('11', '7PM - 8PM'), ('12', '8PM - 9PM')], max_length=100)),
                ('Coupon_code', models.CharField(max_length=20)),
                ('mode', models.CharField(choices=[('1', 'Walkin'), ('2', 'Pickup')], default=1, max_length=2)),
                ('barcode', models.CharField(max_length=255)),
                ('field1', models.CharField(max_length=250)),
                ('field2', models.CharField(max_length=250)),
                ('field3', models.CharField(max_length=250)),
                ('field4', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name_plural': 'List of Laundries',
            },
        ),
        migrations.CreateModel(
            name='pickup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=20)),
                ('service', models.CharField(choices=[('1', 'Dry Clean'), ('2', 'Wash & Fold'), ('3', 'Wash & Iron'), ('4', 'Premium Laundry'), ('5', 'Shoe Cleaning'), ('6', 'Steam Press'), ('7', 'Starching')], max_length=20)),
                ('pickup_date', models.DateField()),
                ('pickup_time', models.CharField(choices=[('1', '9AM - 10AM'), ('2', '10AM - 11AM'), ('3', '11AM - 12PM'), ('4', '12PM - 1PM'), ('5', '1PM - 2PM'), ('6', '2PM - 3PM'), ('7', '3PM - 4PM'), ('8', '4PM - 5PM'), ('9', '5PM - 6PM'), ('10', '6PM - 7PM'), ('11', '7PM - 8PM'), ('12', '8PM - 9PM')], max_length=100)),
                ('delivery_date', models.DateField()),
                ('delivery_time', models.CharField(choices=[('1', '9AM - 10AM'), ('2', '10AM - 11AM'), ('3', '11AM - 12PM'), ('4', '12PM - 1PM'), ('5', '1PM - 2PM'), ('6', '2PM - 3PM'), ('7', '3PM - 4PM'), ('8', '4PM - 5PM'), ('9', '5PM - 6PM'), ('10', '6PM - 7PM'), ('11', '7PM - 8PM'), ('12', '8PM - 9PM')], max_length=100)),
                ('Coupon_code', models.CharField(max_length=20)),
                ('estimated_clothes_quantity', models.CharField(choices=[('1', '20-40'), ('2', '<20'), ('3', ' 40>')], max_length=20)),
                ('heavy_item', models.CharField(choices=[('1', 'Blanket/Quilt'), ('2', 'Carpet'), ('3', 'Curtain')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Prices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('laundry_type', models.CharField(max_length=250)),
                ('category', models.CharField(max_length=250)),
                ('category_type', models.CharField(max_length=250)),
                ('user_type', models.CharField(max_length=250)),
                ('sub_category', models.CharField(max_length=250)),
                ('price', models.FloatField(default=0, max_length=15)),
                ('status', models.CharField(choices=[('1', 'Active'), ('2', 'Inactive')], default=1, max_length=2)),
                ('delete_flag', models.IntegerField(default=0)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('pincode', models.CharField(max_length=100)),
                ('feild_2', models.CharField(max_length=100)),
                ('feild_3', models.CharField(max_length=100)),
                ('feild_4', models.CharField(max_length=100)),
                ('feild_5', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'List of Laundy Prices',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.FloatField(default=0, max_length=15)),
                ('status', models.CharField(choices=[('1', 'Active'), ('2', 'Inactive')], default=1, max_length=2)),
                ('delete_flag', models.IntegerField(default=0)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('pincode', models.CharField(max_length=100)),
                ('feild_2', models.CharField(max_length=100)),
                ('feild_3', models.CharField(max_length=100)),
                ('feild_4', models.CharField(max_length=100)),
                ('feild_5', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'List of Products',
            },
        ),
        migrations.CreateModel(
            name='Rider',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
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
                ('feild_2', models.CharField(max_length=100)),
                ('feild_3', models.CharField(max_length=100)),
                ('feild_4', models.CharField(max_length=100)),
                ('feild_5', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Staffs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('username', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=250)),
                ('password1', models.CharField(max_length=250)),
                ('password2', models.CharField(max_length=250)),
                ('designation', models.CharField(max_length=250)),
                ('location', models.CharField(max_length=100)),
                ('is_staff', models.BooleanField(default=True)),
                ('district', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('franchise_details', models.CharField(max_length=250)),
                ('vendor_details', models.CharField(max_length=250)),
                ('phone', models.IntegerField(blank=True, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=100, verbose_name='Location')),
                ('username', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=250)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('password1', models.CharField(max_length=250)),
                ('password2', models.CharField(max_length=250)),
                ('is_vendor', models.BooleanField(default=True)),
                ('district', models.CharField(max_length=100)),
                ('vendor_city', models.CharField(max_length=100)),
                ('contact_person', models.CharField(max_length=100)),
                ('franchise_details', models.CharField(max_length=250)),
                ('phone', models.IntegerField(blank=True, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('pincode', models.CharField(max_length=100)),
                ('feild_2', models.CharField(max_length=100)),
                ('feild_3', models.CharField(max_length=100)),
                ('feild_4', models.CharField(max_length=100)),
                ('feild_5', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Franchise_branch', models.CharField(max_length=200, null=True)),
                ('Title', models.CharField(max_length=200, null=True)),
                ('Customer_ID', models.CharField(max_length=200, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='tickets')),
                ('Type_of_Tickets', models.CharField(choices=[('1', 'Damaged Garments'), ('2', 'Washing'), ('3', 'Folding'), ('4', 'StreamPress'), ('5', 'Dryer'), ('6', 'Management'), ('7', 'Pickup'), ('8', 'Delivery'), ('9', 'Other')], max_length=200, null=True)),
                ('Description', models.TextField(max_length=4000, null=True)),
                ('Date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.IntegerField(choices=[(1, 'Solved'), (2, 'In-Progress'), (3, 'Pending')], default=3)),
                ('pincode', models.CharField(max_length=100)),
                ('feild_2', models.CharField(max_length=100)),
                ('feild_3', models.CharField(max_length=100)),
                ('feild_4', models.CharField(max_length=100)),
                ('feild_5', models.CharField(max_length=100)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Super_Admin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('pincode', models.CharField(max_length=100)),
                ('feild_2', models.CharField(max_length=100)),
                ('feild_3', models.CharField(max_length=100)),
                ('feild_4', models.CharField(max_length=100)),
                ('feild_5', models.CharField(max_length=100)),
                ('is_admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StockIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('pincode', models.CharField(max_length=100)),
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
        migrations.CreateModel(
            name='LaundryProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0, max_length=15)),
                ('quantity', models.FloatField(default=0, max_length=15)),
                ('total_amount', models.FloatField(max_length=15)),
                ('pincode', models.CharField(max_length=100)),
                ('feild_2', models.CharField(max_length=100)),
                ('feild_3', models.CharField(max_length=100)),
                ('feild_4', models.CharField(max_length=100)),
                ('feild_5', models.CharField(max_length=100)),
                ('laundry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='laundry_fk2', to='smile_dryApp.laundry')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_fk', to='smile_dryApp.products')),
            ],
            options={
                'verbose_name_plural': 'List of Laundry Products',
            },
        ),
        migrations.CreateModel(
            name='LaundryItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0, max_length=15)),
                ('weight', models.FloatField(default=0, max_length=15)),
                ('total_amount', models.FloatField(max_length=15)),
                ('pincode', models.CharField(max_length=100)),
                ('feild_2', models.CharField(max_length=100)),
                ('feild_3', models.CharField(max_length=100)),
                ('feild_4', models.CharField(max_length=100)),
                ('feild_5', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_fk', to='smile_dryApp.prices')),
                ('category_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_type_fk', to='smile_dryApp.prices')),
                ('laundry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='laundry_fk', to='smile_dryApp.laundry')),
                ('laundry_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices_fk', to='smile_dryApp.prices')),
                ('user_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_type_fk', to='smile_dryApp.prices')),
            ],
            options={
                'verbose_name_plural': 'List of Laundry Items',
            },
        ),
    ]
