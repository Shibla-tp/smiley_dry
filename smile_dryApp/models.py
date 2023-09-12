from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from distutils.command.upload import upload
from email.policy import default
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
# from PIL import Image
from django.contrib.auth.base_user import BaseUserManager

from django.db.models import Sum

from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

def validate_phone(value):
    if len(str(value)) != 10:
        raise ValidationError('Phone number must have exactly 10 digits.')

class User(AbstractUser):
    is_admin= models.BooleanField('Is admin', default=False)
    is_franchise = models.BooleanField('Is franchise', default=False)
    is_vendor = models.BooleanField(default=False)
    is_rider = models.BooleanField('Is rider', default=False)
    is_customer = models.BooleanField('Is customer', default=False)
    location = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    phone = models.IntegerField(unique=True, null=True, blank=True, validators=[validate_phone])
    pincode = models.CharField(max_length=100)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    franchise_details = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    photo =  models.FileField(upload_to="Rider_details", null=True, blank=True)
    aadhar =  models.FileField(upload_to="Rider_details", null=True, blank=True)
    license =  models.FileField(upload_to="Rider_details", null=True, blank=True)
    feild_4 = models.CharField(max_length=100)
    feild_5 = models.CharField(max_length=100)
    feild_6 = models.CharField(max_length=100, null=True, blank=True)
class Super_Admin(models.Model):
    id=models.AutoField(primary_key=True)
    is_admin=models.OneToOneField(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    pincode = models.CharField(max_length=100)
    feild_2 = models.CharField(max_length=100)
    feild_3 = models.CharField(max_length=100)
    feild_4 = models.CharField(max_length=100)
    feild_5 = models.CharField(max_length=100)
class Franchise_User(models.Model):
    id=models.AutoField(primary_key=True)
    # user=models.OneToOneField(User,on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    username = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    password1 = models.CharField(max_length=250)
    password2 = models.CharField(max_length=250)
    is_franchise=models.BooleanField(default=True)
    #address=models.TextField()
    # created_at=models.DateTimeField(auto_now_add=True)
    # updated_at=models.DateTimeField(auto_now_add=True)
    # objects=models.Manager()
    
    # # franchise_name = models.CharField('Franchise Name', max_length=100, default='x')
    district = models.CharField(max_length=100)
    franchise_city = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    feild_2 = models.CharField(max_length=100)
    feild_3 = models.CharField(max_length=100)
    feild_4 = models.CharField(max_length=100)
    feild_5 = models.CharField(max_length=100)
    # longitude = models.DecimalField('Longitude', max_digits=9, decimal_places=6, default=0)
    # latitude = models.DecimalField('Latitude', max_digits=9, decimal_places=6, default=0)
    # assigned_vendors = models.ManyToManyField(User, related_name='assigned_franchises', blank=True)

    
    def get_dashboard_url(self):
        return reverse('franchise_dashboard')

class Customer(models.Model):
    id=models.AutoField(primary_key=True)
    # admin=models.OneToOneField(User,on_delete=models.CASCADE)
    location = models.CharField('Location', max_length=100)
    username = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    password1 = models.CharField(max_length=250)
    password2 = models.CharField(max_length=250)
    is_customer=models.BooleanField(default=True)
    district = models.CharField(max_length=100)
    franchise_city = models.ForeignKey("User", default=1, on_delete=models.SET_DEFAULT, null=True, blank=True)
    contact_person = models.CharField(max_length=100)
    phone = models.IntegerField(unique=True, null=True, blank=True, validators=[validate_phone])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    pincode = models.CharField(max_length=100)
    feild_2 = models.CharField(max_length=100)
    feild_3 = models.CharField(max_length=100)
    feild_4 = models.CharField(max_length=100)
    feild_5 = models.CharField(max_length=100)
    #profile_pic=models.FileField()
    #address=models.TextField()
    # created_at=models.DateTimeField(auto_now_add=True)
    # updated_at=models.DateTimeField(auto_now_add=True)
    # objects = models.Manager()
    def __str__(self):
        return str(self.username)
    class Meta:
        verbose_name_plural = "List of Customers"

class Vendor(models.Model):
    # id=models.AutoField(primary_key=True)
    # user=models.OneToOneField(User,on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    location = models.CharField('Location', max_length=100)
    username = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    password1 = models.CharField(max_length=250)
    password2 = models.CharField(max_length=250)
    is_vendor=models.BooleanField(default=True)
    district = models.CharField(max_length=100)
    vendor_city = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    franchise_details= models.CharField(max_length=250)
    phone = models.IntegerField(unique=True, null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    pincode = models.CharField(max_length=100)
    # feild_2 = models.CharField(max_length=100)
    # feild_3 = models.CharField(max_length=100)
    # feild_4 = models.CharField(max_length=100)
    # feild_5 = models.CharField(max_length=100)
    # user_default = User.objects.get(username='User')  # Change this to the actual default user
    # Vendor._meta.get_field('user').default = user_default

    def __str__(self):
        return self.username
    
        
class Rider(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # admin=models.OneToOneField(User,on_delete=models.CASCADE)
    location = models.CharField('Location', max_length=100)
    username = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    password1 = models.CharField(max_length=250)
    password2 = models.CharField(max_length=250)
    is_rider=models.BooleanField(default=True)
    district = models.CharField(max_length=100)
    rider_city = models.CharField(max_length=100)
    franchise_details= models.CharField(max_length=250)
    vendor_details= models.CharField(max_length=250)
    phone = models.IntegerField(unique=True, null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    pincode = models.CharField(max_length=100)
    photo =  models.FileField(upload_to="Rider_details", null=True, blank=True)
    aadhar =  models.FileField(upload_to="Rider_details", null=True, blank=True)
    license =  models.FileField(upload_to="Rider_details", null=True, blank=True)
    feild_5 = models.CharField(max_length=100)
    
class Prices(models.Model):
    laundry_type = models.CharField(max_length=250)
    category = models.CharField(max_length=250)
    category_type = models.CharField(max_length=250)
    user_type = models.CharField(max_length=250)
    sub_category = models.CharField(max_length=250)
    price = models.FloatField(max_length=15, default=0)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)
    pincode = models.CharField(max_length=100)
    image =  models.FileField(upload_to="Categories", null=True, blank=True)
    feild_3 = models.CharField(max_length=100)
    feild_4 = models.CharField(max_length=100)
    feild_5 = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "List of Laundy Prices"

    def __str__(self):
        return str(f"{self.laundry_type}")

class Products(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank= True, null= True)
    price = models.FloatField(max_length=15, default=0)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)
    image = models.FileField(upload_to="Products", null=True, blank=True)
    purchase_rate = models.FloatField(max_length=100)
    GST = models.FloatField(max_length=100)
    sale_price= models.FloatField(max_length=100)
    total_purchase_rate = models.FloatField(max_length=10, default=0)
    feild_2 = models.CharField(max_length=100, default=0)
    feild_3 = models.CharField(max_length=100, default=0)
    feild_4 = models.CharField(max_length=100, default=0)
    feild_5 = models.CharField(max_length=100, default=0)
    

    def __str__(self):
        return str(f"{self.name}")

    
    def available(self):
        try:
            stockin = StockIn.objects.filter(product__id = self.id).aggregate(Sum('quantity'))
            stockin = stockin['quantity__sum']
        except:
            stockin = 0
        try:
            stockout = LaundryProducts.objects.filter(product__id = self.id).aggregate(Sum('quantity'))
            stockout = stockout['quantity__sum']
        except:
            stockout = 0
        stockin = stockin if not stockin is None else 0
        stockout = stockout if not stockout is None else 0
        
        return float(stockin - stockout)

class Productpurchase(models.Model):
    code = models.CharField(max_length=100)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    contact = models.CharField(max_length=250, blank=True, null = True)
    total_amount = models.FloatField(max_length=15)
    total_amount_wgst = models.FloatField(max_length=15, default=0)
    total_amount_cgst = models.FloatField(max_length=15, default=0)
    tendered = models.FloatField(max_length=15)
    status = models.CharField(max_length=2, choices=(('0','Pending'), ('1', 'In-progress'), ('2', 'Done'), ('3', 'Picked Up')), default = 0)
    payment = models.CharField(max_length=2, choices=(('0','Unpaid'), ('1', 'Paid')), default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)

    

    def __str__(self):
        return str(f"{self.code} - {self.client}")

    def change(self):
        change = float(self.tendered) - float(self.total_amount)
        return change

    # def totalItems(self):
    #     try:
    #         Items =  LaundryItems.objects.filter(laundry = self).aggregate(Sum('total_amount'))
    #         Items = Items['total_amount__sum']
    #     except:
    #         Items = 0
    #     return float(Items)
        
    def totalProducts(self):
        try:
            Products =  LaundryProducts.objects.filter(productpurchase = self).aggregate(Sum('total_amount'))
            Products = Products['total_amount__sum']
        except:
            Products = 0
        return float(Products)

    def totalProductswgst(self):
        try:
            Products =  LaundryProducts.objects.filter(productpurchase = self).aggregate(Sum('total_amount_wgst'))
            Products = Products['total_amount_wgst__sum']
        except:
            Products = 0
        return float(Products)

    def totalProductscgst(self):
        try:
            Products =  LaundryProducts.objects.filter(productpurchase = self).aggregate(Sum('total_amount_cgst'))
            Products = Products['total_amount_cgst__sum']
        except:
            Products = 0
        return float(Products)

class LaundryProducts(models.Model):
    productpurchase = models.ForeignKey(Productpurchase, on_delete=models.CASCADE,related_name="productpurchace_fk2")
    product = models.ForeignKey(Products, on_delete=models.CASCADE,related_name="product_fk")
    price = models.FloatField(max_length=15, default=0)
    quantity = models.FloatField(max_length=15, default=0)
    total_amount = models.FloatField(max_length=15)
    total_amount_wgst = models.FloatField(max_length=15, default=0)
    total_amount_cgst = models.FloatField(max_length=15, default=0)
    pincode = models.CharField(max_length=100)
    feild_2 = models.CharField(max_length=100)
    feild_3 = models.CharField(max_length=100)
    feild_4 = models.CharField(max_length=100)
    feild_5 = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "List of Laundry Products"

    def __str__(self):
        return str(f"{self.productpurchase.code} - {self.product.name}")

class Staffs(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    id=models.AutoField(primary_key=True)
    # admin=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    username = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    password1 = models.CharField(max_length=250)
    password2 = models.CharField(max_length=250)
    designation= models.CharField(max_length=250)
    location = models.CharField(max_length=100)
    is_staff= models.BooleanField(default=True)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address=models.TextField()
    franchise_details= models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=True)
    vendor_details= models.CharField(max_length=250)
    phone = models.IntegerField(unique=True, null=True, blank=True, validators=[validate_phone])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    photo =  models.FileField(upload_to="Staff_details", null=True, blank=True)
    aadhar =  models.FileField(upload_to="Staff_details", null=True, blank=True)
    pan_card =  models.FileField(upload_to="Staff_details", null=True, blank=True)

class Attendance(models.Model):
    # classIns = models.ForeignKey(Class,on_delete=models.CASCADE)
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    type = models.CharField(max_length=250, choices = [('1','Present'),('2','Absent')], default = 1 )
    date_updated = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.classIns.name + "  " +self.student.student_code

class StockIn(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.FloatField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)
    pincode = models.CharField(max_length=100)
    feild_2 = models.CharField(max_length=100)
    feild_3 = models.CharField(max_length=100)
    feild_4 = models.CharField(max_length=100)
    feild_5 = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "List of Stock-In"

    def __str__(self):
        return str(f"{self.product}")



class Laundry(models.Model):
    code = models.CharField(max_length=100)
    client = models.ForeignKey("Customer", default=1, on_delete=models.SET_DEFAULT, null=True, blank=True, related_name="client_user")
    contact = models.CharField(max_length=250, blank=True, null = True)
    total_amount = models.FloatField(max_length=15)
    tendered = models.FloatField(max_length=15)
    # discount = models.FloatField(max_length=15, blank=True, null = True)
    status = models.CharField(max_length=2, choices=(('0','Pending'), ('1', 'In-progress'), ('2', 'Done'), ('3', 'Picked Up'),('4','Canceled')), default = 0)
    payment = models.CharField(max_length=2, choices=(('0','Unpaid'), ('1', 'Paid')), default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)
    pickup_date=models.DateField(default=timezone.now)
    delivery_date=models.DateField()
    Coupon_code=models.CharField(max_length=20)
    mode = models.CharField(max_length=2, choices=(('1','Walkin'), ('2','Pickup')), default = 1)
    barcode = models.CharField(max_length=255)
    franchise_details=  models.ForeignKey("User", default=1, on_delete=models.SET_DEFAULT, null=True, blank=True, related_name="franchise_user")
    vendor_details= models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, related_name="vendor_user")
    pincode = models.IntegerField()
    SLOT = [
        ('1', '9AM - 10AM'),
        ('2', '10AM - 11AM'),
        ('3', '11AM - 12PM'),
        ('4', '12PM - 1PM'),
        ('5', '1PM - 2PM'),
        ('6', '2PM - 3PM'),
        ('7', '3PM - 4PM'),
        ('8', '4PM - 5PM'),
        ('9', '5PM - 6PM'),
        ('10', '6PM - 7PM'),
        ('11', '7PM - 8PM'),
        ('12', '8PM - 9PM')
]
    pickup_time=models.CharField(max_length=100, choices=SLOT)
    delivery_time=models.CharField(max_length=100, choices=SLOT)
    address = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "List of Laundries"

    def __str__(self):
        return str(f"{self.code} - {self.client}")

    def change(self):
        change = float(self.tendered) - float(self.total_amount)
        return change

    def totalItems(self):
        try:
            Items =  LaundryItems.objects.filter(laundry = self).aggregate(Sum('total_amount'))
            Items = Items['total_amount__sum']
        except:
            Items = 0
        return Items
        
    # def totalProducts(self):
    #     try:
    #         Products =  LaundryProducts.objects.filter(laundry = self).aggregate(Sum('total_amount'))
    #         Products = Products['total_amount__sum']
    #     except:
    #         Products = 0
    #     return float(Products)

class LaundryItems(models.Model):
    laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE,related_name="laundry_fk")
    laundry_type = models.ForeignKey(Prices, on_delete=models.CASCADE,related_name="prices_fk")
    category = models.ForeignKey(Prices, on_delete=models.CASCADE, related_name="category_fk")
    category_type = models.ForeignKey(Prices, on_delete=models.CASCADE, related_name="category_type_fk")
    user_type = models.ForeignKey(Prices, on_delete=models.CASCADE, related_name="user_type_fk")
    price = models.FloatField(max_length=15, default=0)
    weight = models.FloatField(max_length=15, default=0)
    total_amount = models.FloatField(max_length=15)
  

    class Meta:
        verbose_name_plural = "List of Laundry Items"

    def __str__(self):
        return str(f"{self.laundry.code} - {self.laundry_type.laundry_type}")




class Tickets(models.Model):
    STATUS =((1,'Solved'),(2, 'In-Progress'),(3,'Pending'))
    TYPE=(('1',"Damaged Garments"),('2',"Washing"),('3',"Folding"),('4',"StreamPress"),('5',"Dryer"),('6',"Management"),('7',"Pickup"),('8',"Delivery"),('9',"Other"))
    
    Franchise_branch = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tickets', null=True, blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    Title=models.CharField(max_length=200,blank=False,null=True)
    Customer_ID=models.CharField(max_length=200,blank=False,null=True)
    image =  models.FileField(upload_to="tickets", null=True, blank=True)
    Type_of_Tickets=models.CharField(choices=TYPE,null=True,max_length=200)
    Description=models.TextField(max_length=4000,blank=False,null=True)
    Date_time =  models.DateTimeField(default = timezone.now)
    status=models.IntegerField(choices=STATUS,default=3)
    pincode = models.CharField(max_length=100)
    feild_2 = models.CharField(max_length=100)
    feild_3 = models.CharField(max_length=100)
    feild_4 = models.CharField(max_length=100)
    feild_5 = models.CharField(max_length=100)
   
    def __init__(self, *args, **kwargs):
        super(Tickets, self).__init__(*args, **kwargs)
        self.__status = self.status

    def save(self, *args, **kwargs):
        if self.status and not self.__status:
            self.active_from = datetime.now()
        super(Tickets, self).save(*args, **kwargs)
    
    def __str__(self):
     	return self.get_Type_of_Tickets_display()
    def __str__(self):
 	    return str(self.user)

#products in Franchise
class FranchiseProducts(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank= True, null= True)
    price = models.FloatField(max_length=15, default=0)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)
    franchise_details = models.ForeignKey(User, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=100)
    # image =  models.FileField(upload_to="tickets", null=True, blank=True)
    image = models.FileField(upload_to="Franchise_Products", null=True, blank=True)
    feild_3 = models.CharField(max_length=100)
    feild_4 = models.CharField(max_length=100)
    feild_5 = models.CharField(max_length=100)
    # class Meta:
    #     verbose_name_plural = "List of Products"

    def __str__(self):
        return str(f"{self.name}")
    
    def __str__(self):
        return str(f"{self.franchise_details}")

    def available(self):
        try:
            franchisestockin = FranchiseStockIn.objects.filter(franchiseproduct__id = self.id).aggregate(Sum('quantity'))
            franchisestockin = franchisestockin['quantity__sum']
        except:
            stockin = 0

        try:
            franchisestockout = FranchiseStockOut.objects.filter(franchiseproduct__id = self.id).aggregate(Sum('quantity'))
            franchisestockout = franchisestockout['quantity__sum']
        except:
            franchisestockout = 0
        franchisestockin = franchisestockin if not franchisestockin is None else 0
        franchisestockout = franchisestockout if not franchisestockout is None else 0
        
        return float(franchisestockin - franchisestockout)
    


class FranchiseStockIn(models.Model):
    franchiseproduct = models.ForeignKey(FranchiseProducts, on_delete=models.CASCADE)
    quantity = models.FloatField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)
    franchise_details= models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, related_name="stokckin_franchise")
    feild_2 = models.CharField(max_length=100)
    feild_3 = models.CharField(max_length=100)
    feild_4 = models.CharField(max_length=100)
    feild_5 = models.CharField(max_length=100)
    # class Meta:
    #     verbose_name_plural = "List of Stock-In"

    # def __str__(self):
    #     return str(f"{self.franchiseproduct}")

class FranchiseStockOut(models.Model):
    franchiseproduct = models.ForeignKey(FranchiseProducts, on_delete=models.CASCADE)
    quantity = models.FloatField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)
    franchise_details= models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, related_name="stokckout_franchise")
    feild_2 = models.CharField(max_length=100)
    feild_3 = models.CharField(max_length=100)
    feild_4 = models.CharField(max_length=100)
    feild_5 = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "List of Stock-out"

    # def __str__(self):
    #     return str(f"{self.franchiseproduct}")



class UsedProducts(models.Model):
    # laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE,related_name="laundry_fk2")
    franchiseproduct = models.ForeignKey(FranchiseProducts, on_delete=models.CASCADE,related_name="franchiseproduct_fk")
    price = models.FloatField(max_length=15, default=0)
    quantity = models.FloatField(max_length=15, default=0)
    total_amount = models.FloatField(max_length=15)
    franchise_details= models.CharField(max_length=250)
    feild_2 = models.CharField(max_length=100)
    feild_3 = models.CharField(max_length=100)
    feild_4 = models.CharField(max_length=100)
    feild_5 = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "List of Laundry Products"

    # def __str__(self):
    #     return str(f"{self.laundry.code} - {self.product.name}")




# walkin & pickup===start
# walkin model
SERVICE_CHOICES =[
        ('1', 'Dry Clean'),
        ('2', 'Wash & Fold'),
        ('3', 'Wash & Iron'),
        ('4', 'Premium Laundry'),
        ('5', 'Shoe Cleaning'),
        ('6', 'Steam Press'),
        ('7', 'Starching'),
    ]

SLOT = [
        ('1', '9AM - 10AM'),
        ('2', '10AM - 11AM'),
        ('3', '11AM - 12PM'),
        ('4', '12PM - 1PM'),
        ('5', '1PM - 2PM'),
        ('6', '2PM - 3PM'),
        ('7', '3PM - 4PM'),
        ('8', '4PM - 5PM'),
        ('9', '5PM - 6PM'),
        ('10', '6PM - 7PM'),
        ('11', '7PM - 8PM'),
        ('12', '8PM - 9PM')
]
ESTIMATED_QUANTITY_CHOICES = [
    ('1', '20-40'),
    ('2', '<20'),
    ('3', ' 40>'),
]

HEAVY_ITEM_CHOICES = [
    ('1', 'Blanket/Quilt'),
    ('2', 'Carpet'),
    ('3', 'Curtain'),
]
class B2C(models.Model):

    customer_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    service=models.CharField(max_length=20,choices=SERVICE_CHOICES)
    delivery_date=models.DateField()
    delivery_time=models.CharField(max_length=100, choices=SLOT)
    Coupon_code=models.CharField(max_length=20)

   

# pickup model
class pickup(models.Model):

    customer_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    service=models.CharField(max_length=20,choices=SERVICE_CHOICES)
    pickup_date=models.DateField()
    pickup_time=models.CharField(max_length=100, choices=SLOT)
    delivery_date=models.DateField()
    delivery_time=models.CharField(max_length=100, choices=SLOT)
    Coupon_code=models.CharField(max_length=20)
    estimated_clothes_quantity = models.CharField(max_length=20, choices=ESTIMATED_QUANTITY_CHOICES)
    heavy_item = models.CharField(max_length=20, choices=HEAVY_ITEM_CHOICES)
# walkin & pickup===end

# chat
class chatMessages(models.Model):
    user_from = models.ForeignKey(User,
        on_delete=models.CASCADE,related_name="+")
    user_to = models.ForeignKey(User,
        on_delete=models.CASCADE,related_name="+")
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message
# cctv link model===start
class CCTV(models.Model):
    Franchise_name = models.CharField(max_length=100)
    Live_stream_url = models.URLField()

    def __str__(self):
        return self.Franchise_name

# cctv link model===end
#Coupon_code
class Coupon(models.Model):
    code = models.CharField(max_length=100, unique = True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    discount_type = models.CharField(max_length=2, choices=(('1','Percentage'), ('2','Fixed Amount'), ('3','Free Shipping')), default = 1)
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    active = models.BooleanField(default=False)
    user_limit= models.IntegerField()
    status = models.CharField(max_length=2, choices=(('1','Eanbled'), ('2','Disabled')), default = 1)
    franchise_details = models.ForeignKey("User", default=1, on_delete=models.SET_DEFAULT, null=True, blank=True)
    feild_2 = models.CharField(max_length=100)
    feild_3 = models.CharField(max_length=100)
    feild_4 = models.CharField(max_length=100)
    feild_5 = models.CharField(max_length=100)

    def __str__(self):
        return self.code

class LaundryCoupons(models.Model):
    laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE,related_name="laundry_fk2")
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE,related_name="coupon_fk")
    discount = models.FloatField(max_length=15, default=0)
    discount_type = models.CharField(max_length=2, choices=(('1','Percentage'), ('2','Fixed Amount'), ('3','Free Shipping')), default = 1)
    total_amount = models.FloatField(max_length=15)
    total_amount_wgst = models.FloatField(max_length=15, default=0)
    total_amount_cgst = models.FloatField(max_length=15, default=0)
    pincode = models.CharField(max_length=100)
    feild_2 = models.CharField(max_length=100)
    feild_3 = models.CharField(max_length=100)
    feild_4 = models.CharField(max_length=100)
    feild_5 = models.CharField(max_length=100)
    feild_6 = models.CharField(max_length=100)
    feild_7 = models.CharField(max_length=100)
    feild_8 = models.CharField(max_length=100)
    feild_9 = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "List of Laundry Products"

    # def __str__(self):
    #     return str(f"{self.productpurchace.code} - {self.product.name}")

class Banners(models.Model):
    banner_type = models.CharField(max_length=250, choices=(('Home Page Banner','Home Page Banner'), ('Offer Banner','Offer Banner'), ('Website Offer Banner','Website Offer Banner')), default = 'Home Page Banner')
    title = models.CharField(max_length=250)
    offer = models.FloatField(max_length=15, default=0)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)
    image =  models.FileField(upload_to="Banners", null=True, blank=True)
    mobile_image =  models.FileField(upload_to="Categories", null=True, blank=True)
    description  =     description = models.TextField(blank= True, null= True)
    feild_2  = models.CharField(max_length=100)
    feild_3 = models.CharField(max_length=100)
    feild_4 = models.CharField(max_length=100)
    feild_5 = models.CharField(max_length=100)

class Contact(models.Model):
    Address = models.TextField(max_length=250)
    phone = models.IntegerField(unique=True, null=True, blank=True, validators=[validate_phone])
    alternative_phone = models.IntegerField(unique=True, null=True, blank=True, validators=[validate_phone])
    email_1 = models.EmailField(max_length=250)
    email_2 = models.EmailField(max_length=250)
    email_3 = models.EmailField(max_length=250)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)
    image =  models.FileField(upload_to="Banners", null=True, blank=True)
    description  = models.TextField(blank= True, null= True)
    feild_2  = models.CharField(max_length=100)
    feild_3 = models.CharField(max_length=100)
    feild_4 = models.CharField(max_length=100)
    feild_5 = models.CharField(max_length=100)
    feild_6  = models.CharField(max_length=100)
    feild_7 = models.CharField(max_length=100)
    feild_8 = models.CharField(max_length=100)
    feild_9 = models.CharField(max_length=100)
    
    
class TermsCondition(models.Model):
    description = models.TextField(max_length=2000)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)
    feild_2  = models.CharField(max_length=100)
    feild_3 = models.CharField(max_length=100)
    feild_4 = models.CharField(max_length=100)
    feild_5 = models.CharField(max_length=100)
    feild_6  = models.CharField(max_length=100)
    feild_7 = models.CharField(max_length=100)
    feild_8 = models.CharField(max_length=100)
    feild_9 = models.CharField(max_length=100)
    
class AboutUs(models.Model):
    description = models.TextField(max_length=2000)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(auto_now = True)
    feild_2  = models.CharField(max_length=100)
    feild_3 = models.CharField(max_length=100)
    feild_4 = models.CharField(max_length=100)
    feild_5 = models.CharField(max_length=100)
    feild_6  = models.CharField(max_length=100)
    feild_7 = models.CharField(max_length=100)
    feild_8 = models.CharField(max_length=100)
    feild_9 = models.CharField(max_length=100)
       

class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    heading = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Add the is_read field
    quantity = models.FloatField(default = 0)
    def __str__(self):
        return f"Notification from {self.sender.username}"

class Franchise_Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    heading = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Add the is_read field
    quantity = models.FloatField(default = 0)
    def __str__(self):
        return f"Notification from {self.sender.username}"


class Timeslot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_of_week = models.CharField(max_length=10, choices=[
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ])
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.day_of_week} - {self.start_time.strftime("%I:%M %p")} to {self.end_time.strftime("%I:%M %p")}'