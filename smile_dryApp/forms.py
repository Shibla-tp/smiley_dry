from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Tickets, Franchise_User, Customer, Vendor, Rider, Staffs, Banners
from datetime import datetime
from tabnanny import check
from django import forms
from numpy import require
from smile_dryApp import models
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm, UserChangeForm
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
User = get_user_model()
# tickets
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import datetime
from django.db.models import CharField
from django.db import transaction
class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = '__all__'
'''class SaveUser(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('is_customer',)'''
class SaveUser(forms.ModelForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    password1 = forms.CharField(max_length=250)
    password2 = forms.CharField(max_length=250)
    is_customer=forms.BooleanField(initial=False)
    
    class Meta:
        model = Customer
        fields = ('email', 'username','first_name', 'last_name','password1', 'password2', 'is_customer','district', 'location','phone', 'franchise_city','pincode' )
# class UpdatePasswords(PasswordChangeForm):
#     old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Old Password")
#     new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="New Password")
#     new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Confirm New Password")
#     class Meta:
#         model = User
#         fields = ('old_password','new_password1', 'new_password2')
class Savefranchise(UserCreationForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    password1 = forms.CharField(max_length=250)
    password2 = forms.CharField(max_length=250)
    is_franchise=forms.BooleanField(initial=False)
    location = forms.CharField(max_length=250,help_text="The Location field is required.")
    district =  forms.CharField(max_length=250,help_text="The District field is required.")
    status = forms.CharField(max_length=2)
    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name','password1', 'password2', 'is_franchise', 'district', 'location',  'contact_person', 'city','phone', 'status', 'pincode')
class Updatefranchise(UserChangeForm):
    # username = forms.CharField(max_length=250,help_text="The Username field is required.")
    # email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    # first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    # last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    status = forms.CharField(max_length=2)
    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name', 'location', 'district', 'contact_person', 'city', 'phone', 'status','pincode')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")

# class Savevendor(UserCreationForm):
#     username = forms.CharField(max_length=250,help_text="The Username field is required.")
#     email = forms.EmailField(max_length=250,help_text="The Email field is required.")
#     first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
#     last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
#     password1 = forms.CharField(max_length=250)
#     password2 = forms.CharField(max_length=250)
#     is_vendor=forms.BooleanField(initial=False)
    
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('email', 'username','first_name', 'last_name', 'district', 'location',  'contact_person', 'city', 'phone', 'franchise_details', )

class Savevendor(UserCreationForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    password1 = forms.CharField(max_length=250)
    password2 = forms.CharField(max_length=250)
    is_vendor=forms.BooleanField(initial=False)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username','first_name', 'last_name','password1', 'password2', 'is_vendor', 'district', 'location',  'contact_person', 'phone','pincode','city','franchise_details')
    
    # def save(self):
    #     user = super().save(commit=False)
    #     user.is_vendor = True
    #     user.save()

    #     vendor = Vendor.objects.create(user=user)

    #     franchise_details = self.cleaned_data.get('franchise_details', '')
    #     vendor.franchise_details = franchise_details

    #     vendor.save()  # Save the vendor object with updated fields

    #     return user
        
from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import User  # Assuming you have imported your User model

class Updatevendor(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'is_vendor', 'district', 'location', 'contact_person', 'phone', 'pincode', 'city', 'franchise_details')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['email'].disabled = True  # Disable editing of email field
    #     self.fields['username'].disabled = True  # Disable editing of username field
    #     self.fields['is_vendor'].disabled = True  # Disable editing of is_vendor field


class Saverider(UserCreationForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    password1 = forms.CharField(max_length=250)
    password2 = forms.CharField(max_length=250)
    is_rider=forms.BooleanField(initial=False)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username','first_name', 'last_name','password1', 'password2', 'is_rider', 'district', 'location', 'city', 'phone', 'franchise_details','pincode','photo','aadhar','license')

        
from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import User  # Assuming you have imported your User model

class Updaterider(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name', 'is_rider', 'district', 'location', 'city', 'phone', 'franchise_details','pincode','photo','aadhar','license')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['email'].disabled = True  # Disable editing of email field
        # self.fields['username'].disabled = True  # Disable editing of username field
        self.fields['is_rider'].disabled = True  # Disable editing of is_vendor field


# class Saverider(forms.ModelForm):
#     username = forms.CharField(max_length=250,help_text="The Username field is required.")
#     email = forms.EmailField(max_length=250,help_text="The Email field is required.")
#     first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
#     last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
#     password1 = forms.CharField(max_length=250)
#     password2 = forms.CharField(max_length=250)
#     is_rider=forms.BooleanField(initial=False)
    
#     class Meta:
#         model = Rider
#         fields = ('email', 'username','first_name', 'last_name','password1', 'password2', 'is_rider', 'district', 'location', 'rider_city', 'phone', 'franchise_details','pincode')

class UpdateProfile(UserChangeForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    current_password = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name')

    def clean_current_password(self):
        if not self.instance.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError(f"Password is Incorrect")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")

class UpdateFranchiseProfile(UserChangeForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    current_password = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name', 'district', 'location',  'contact_person', 'city','phone')

    def clean_current_password(self):
        if not self.instance.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError(f"Password is Incorrect")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")

class UpdateUser(forms.ModelForm):
    # username = forms.CharField(max_length=250,help_text="The Username field is required.")
    # email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    # first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    # last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")

    class Meta:
        model = Customer
        fields = ('email', 'username','first_name', 'last_name', 'district', 'location','phone', )

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = Customer.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = Customer.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")



# class Updatevendor(forms.ModelForm):
#     # username = forms.CharField(max_length=250,help_text="The Username field is required.")
#     # email = forms.EmailField(max_length=250,help_text="The Email field is required.")
#     # first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
#     # last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")

#     class Meta:
#        model = Vendor
#        fields = ('email', 'username','first_name', 'last_name', 'district', 'location',  'contact_person', 'vendor_city', 'phone', 'franchise_details', )


#     def clean_email(self):
#         email = self.cleaned_data['email']
#         try:
#             user = Vendor.objects.exclude(id=self.cleaned_data['id']).get(email = email)
#         except Exception as e:
#             return email
#         raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

#     def clean_username(self):
#         username = self.cleaned_data['username']
#         try:
#             user = Vendor.objects.exclude(id=self.cleaned_data['id']).get(username = username)
#         except Exception as e:
#             return username
#         raise forms.ValidationError(f"The {user.username} mail is already exists/taken")
        
# class Updaterider(forms.ModelForm):
#     # username = forms.CharField(max_length=250,help_text="The Username field is required.")
#     # email = forms.EmailField(max_length=250,help_text="The Email field is required.")
#     # first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
#     # last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")

#     class Meta:
#         model = Rider
#         fields = ('email', 'username','first_name', 'last_name', 'district', 'location', 'phone', 'franchise_details', 'rider_city')

#     def clean_email(self):
#         email = self.cleaned_data['email']
#         try:
#             user = Rider.objects.exclude(id=self.cleaned_data['id']).get(email = email)
#         except Exception as e:
#             return email
#         raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

#     def clean_username(self):
#         username = self.cleaned_data['username']
#         try:
#             user = Rider.objects.exclude(id=self.cleaned_data['id']).get(username = username)
#         except Exception as e:
#             return username
#         raise forms.ValidationError(f"The {user.username} mail is already exists/taken")
        
class UpdatePasswords(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Confirm New Password")
    class Meta:
        model = User
        fields = ('old_password','new_password1', 'new_password2')

class SavePrice(forms.ModelForm):
    laundry_type = forms.CharField(max_length=250)
    price = forms.CharField(max_length=250)
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.Prices
        fields = ('laundry_type', 'category', 'category_type', 'user_type', 'price', 'status','image' )

    # def clean_laundry_type(self):
    #     id = self.data['id'] if (self.data['id']).isnumeric() else 0
    #     laundry_type = self.cleaned_data['laundry_type']
    #     if id > 0:
    #         price = models.Prices.objects.exclude(id = id).get(laundry_type = laundry_type, delete_flag = 0)
    #     else:
    #         price = models.Prices.objects.get(laundry_type = laundry_type, delete_flag = 0)
        # try:
        #     if id > 0:
        #         price = models.Prices.objects.exclude(id = id).get(laundry_type = laundry_type, delete_flag = 0)
        #     else:
        #         price = models.Prices.objects.get(laundry_type = laundry_type, delete_flag = 0)
        # except:
        #     return laundry_type
        # raise forms.ValidationError("Laundry Type already exists.")

class SaveProductsFranchise(forms.ModelForm):
    name = forms.CharField(max_length=250)
    description = forms.CharField(max_length=250)
    price = forms.CharField(max_length=250)
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.FranchiseProducts
        fields = ('name', 'description', 'price', 'status', 'image' )

    # def clean_name(self):
    #     id = self.data['id'] if (self.data['id']).isnumeric() else 0
    #     name = self.cleaned_data['name']
    #     try:
    #         if id > 0:
    #             franchiseproduct = models.FranchiseProducts.objects.exclude(id = id, franchise_details=franchise_details).get(name = name, delete_flag = 0)
    #         else:
    #             franchiseproduct = models.FranchiseProducts.objects.get(name = name, delete_flag = 0)
    #     except:
    #         return name
    #     raise forms.ValidationError("Product Name already exists.")

    
    def clean_name(self):
        id = self.cleaned_data.get('id')  
        name = self.cleaned_data.get('name')
        franchise_details = self.cleaned_data.get('franchise_details') 
        id = int(id) if id and id.isnumeric() else 0

        
        query = models.FranchiseProducts.objects.filter(name=name, franchise_details=franchise_details, delete_flag=0)

        if id > 0:
            query = query.exclude(id=id)

        existing_entry = query.first()

        if existing_entry:
            
            raise forms.ValidationError("Product Name already exists for this franchise.")

        
        return name

class SaveProducts(forms.ModelForm):
    name = forms.CharField(max_length=250)
    description = forms.CharField(max_length=250)
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.Products
        fields = ('name', 'description', 'purchase_rate', 'GST', 'sale_price', 'status', 'image')

    def clean_name(self):
        id = self.data['id'] if (self.data['id']).isnumeric() else 0
        name = self.cleaned_data['name']
        try:
            if id > 0:
                product = models.Products.objects.exclude(id = id).get(name = name, delete_flag = 0)
            else:
                product = models.Products.objects.get(name = name, delete_flag = 0)
        except:
            return name
        raise forms.ValidationError("Product Name already exists.")

class SaveProductpurchase(forms.ModelForm):
    code = forms.CharField(max_length=250)
    # client = forms.CharField(max_length=250)
    contact = forms.CharField(max_length=250,required= False)
    status = forms.CharField(max_length=2)
    payment = forms.CharField(max_length=2)
    total_amount = forms.CharField(max_length=250)
    tendered = forms.CharField(max_length=250)
    

    class Meta:
        model = models.Productpurchase
        fields = ('code', 'client', 'contact', 'status', 'payment', 'total_amount', 'tendered','total_amount_wgst', 'total_amount_cgst')

    def clean_code(self):
        code = self.cleaned_data['code']
       
        if code == 'generate':
            pref = datetime.datetime.now().strftime('%y%m%d')
            code = 1
            while True:
                try:
                    check = models.Productpurchase.objects.get(code = f"{pref}{code:05d}")
                    code = code + 1
                except:
                    return f"{pref}{code:05d}"
                    break
        else:
            return code
    
    def clean_payment(self):
        tendered = float(self.data['tendered'])
        if tendered > 0:
            return 1
        else:
            return 0

    def save(self):
        instance = self.instance
        Products = []
        Items = []
        # print(f"{self.data}")
        # if 'price_id[]' in self.data:
        #     for k, val in enumerate(self.data.getlist('price_id[]')):
        #         prices = models.Prices.objects.get(id= val)
        #         price = self.data.getlist('laundry_price[]')[k]
        #         weight = self.data.getlist('laundry_weight[]')[k]
        #         total = float(price) * float(weight)
        #         try:
        #             Items.append(models.LaundryItems(laundry = instance, laundry_type = prices, price = price,weight = weight, total_amount = total))
        #             print("LaundryItems..")
        #         except Exception as err:
        #             print(err)
        #             return False
        if 'product_id[]' in self.data:
            for k, val in enumerate(self.data.getlist('product_id[]')):
                product = models.Products.objects.get(id= val)
                price = self.data.getlist('product_price[]')[k]
                sale_price = self.data.getlist('product_sale_price[]')[k]
                GST = self.data.getlist('product_GST[]')[k]
                qty = self.data.getlist('product_quantity[]')[k]
                total = float(price) * float(qty)
                total_wgst = float(sale_price) * float(qty)
                total_cgst = float(sale_price) * float(qty) * float(GST) / 200
                try:
                    Products.append(models.LaundryProducts(productpurchase = instance, product = product, price = price, quantity = qty, total_amount = total, total_amount_wgst = total_wgst, total_amount_cgst = total_cgst))
                    print("LaundryProducts..")
                except Exception as err:
                    print(err)
                    return False
        try:
            instance.save()
            models.LaundryProducts.objects.filter(productpurchase = instance).delete()
            models.LaundryProducts.objects.bulk_create(Products)
            models.Productpurchase.objects.filter(productpurchase = instance).delete()
            models.Productpurchase.objects.bulk_create(Items)
        except Exception as err:
            print(err)
            return False



class SaveStockIn(forms.ModelForm):
    product = forms.CharField(max_length=250)
    quantity = forms.CharField(max_length=250)
    
    class Meta:
        model = models.StockIn
        fields = ('product', 'quantity')

    def clean_product(self):
        pid = self.cleaned_data['product']
        try:
            product = models.Products.objects.get(id = pid, delete_flag = 0)
            return product
        except:
            raise forms.ValidationError("Product is Invalid.")

class SaveStockInFranchise(forms.ModelForm):
    franchiseproduct = forms.CharField(max_length=250)
    quantity = forms.CharField(max_length=250)
    # franchise_details= forms.CharField(max_length=250)

    class Meta:
        model = models.FranchiseStockIn
        fields = ('franchiseproduct', 'quantity', 'franchise_details')

    def clean_franchiseproduct(self):
        pid = self.cleaned_data['franchiseproduct']
        try:
            franchiseproduct = models.FranchiseProducts.objects.get(id = pid, delete_flag = 0)
            return franchiseproduct
        except:
            raise forms.ValidationError("Product is Invalid.")

class SaveStockOutFranchise(forms.ModelForm):
    franchiseproduct = forms.CharField(max_length=250)
    quantity = forms.CharField(max_length=250)
    # franchise_details= forms.CharField(max_length=250)

    class Meta:
        model = models.FranchiseStockOut
        fields = ('franchiseproduct', 'quantity', 'franchise_details')

    def clean_franchiseproduct(self):
        pid = self.cleaned_data['franchiseproduct']
        try:
            franchiseproduct = models.FranchiseProducts.objects.get(id = pid, delete_flag = 0)
            return franchiseproduct
        except:
            raise forms.ValidationError("Product is Invalid.")   
    
class SaveLaundry(forms.ModelForm):
    code = forms.CharField(max_length=250)
    # client = forms.CharField(max_length=250)
    contact = forms.CharField(max_length=250,required= False)
    status = forms.CharField(max_length=2)
    payment = forms.CharField(max_length=2)
    total_amount = forms.CharField(max_length=250)
    tendered = forms.CharField(max_length=250)
    
    delivery_date=forms.DateField()
    Coupon_code=forms.CharField(max_length=20, required=False )
    mode = forms.CharField(max_length=20)
    barcode = forms.CharField(max_length=255, required=False )
    # pickup_time = forms.CharField(max_length=100, required=False)
    delivery_time = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)
    # franchise_details = forms.CharField(max_length=255)
    pincode = forms.IntegerField()

    class Meta:
        model = models.Laundry
        fields = ('code', 'client', 'contact', 'status', 'payment', 'total_amount', 'tendered','delivery_date','Coupon_code','mode','barcode','delivery_time','address','pincode','franchise_details')

    def clean_code(self):
        code = self.cleaned_data['code']
       
        if code == 'generate':
            pref = datetime.datetime.now().strftime('%y%m%d')
            code = 1
            while True:
                try:
                    check = models.Laundry.objects.get(code = f"{pref}{code:05d}")
                    code = code + 1
                except:
                    return f"{pref}{code:05d}"
                    break
        else:
            return code
    
    def clean_payment(self):
        tendered = float(self.data['tendered'])
        if tendered > 0:
            return 1
        else:
            return 0

    def save(self):
        instance = self.instance
        Products = []
        Items = []
        Coupons = []
        # print(f"{self.data}")
        if 'price_id[]' in self.data:
            for k, val in enumerate(self.data.getlist('price_id[]')):
                prices = models.Prices.objects.get(id= val)
                price = self.data.getlist('laundry_price[]')[k]
                weight = self.data.getlist('laundry_weight[]')[k]
                total = float(price) * float(weight)
                try:
                    Items.append(models.LaundryItems(laundry = instance, laundry_type = prices,category=prices,category_type=prices,user_type=prices, price = price,weight = weight, total_amount = total))
                    print("LaundryItems..")
                except Exception as err:
                    print(err)
                    return False
        try:
            instance.save()
            models.LaundryItems.objects.filter(laundry = instance).delete()
            models.LaundryItems.objects.bulk_create(Items)
        except Exception as err:
            print(err)
            return False
        if 'coupon_id[]' in self.data:
            for k, val in enumerate(self.data.getlist('coupon_id[]')):
                coupon = models.Coupon.objects.get(id= val)
                discount_type = self.data.getlist('coupon_discount_type[]')[k]
                discount = self.data.getlist('coupon_discount[]')[k]
                
                try:
                    laundry_item = models.LaundryItems.objects.get(laundry=instance)
                    total_amount = laundry_item.total_amount
                except models.LaundryItems.DoesNotExist:
                    total_amount = 0
                
                if discount_type == '1':  # Percentage discount
                    discount = (total_amount * float(discount)) / 100  # Convert discount to float
                elif discount_type == '2':  # Fixed amount discount
                    discount = float(discount)  # Convert discount to float

                total = total_amount - discount  # Now subtraction should work

                print(total)
                
                try:
                    Coupons.append(models.LaundryCoupons(laundry = instance, coupon = coupon, discount_type = discount_type, discount = discount, total_amount = total))
                    print("Laundrycoupons..")
                except Exception as err:
                    print(err)
                    return False
        try:
            instance.save()
            models.LaundryCoupons.objects.filter(laundry = instance).delete()
            models.LaundryCoupons.objects.bulk_create(Coupons)
          
        except Exception as err:
            print(err)
            return False

            raise forms.ValidationError("Coupon is Invalid.")


            
class SaveLaundryPickup(forms.ModelForm):
    code = forms.CharField(max_length=250)
    # client = forms.CharField(max_length=250)
    contact = forms.CharField(max_length=250,required= False)
    status = forms.CharField(max_length=2)
    payment = forms.CharField(max_length=2)
    total_amount = forms.CharField(max_length=250)
    tendered = forms.CharField(max_length=250)
    pickup_date=forms.DateField(required=False)
    delivery_date=forms.DateField()
    Coupon_code=forms.CharField(max_length=20, required=False )
    mode = forms.CharField(max_length=20)
    barcode = forms.CharField(max_length=255, required=False )
    pickup_time = forms.CharField(max_length=100, required=False )
    delivery_time = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)
    # franchise_details = forms.CharField(max_length=255)
    pincode = forms.IntegerField()

    class Meta:
        model = models.Laundry
        fields = ('code', 'client', 'contact', 'status', 'payment', 'total_amount', 'tendered','pickup_date','delivery_date','Coupon_code','mode','barcode','pickup_time','delivery_time','address','pincode','franchise_details')

    def clean_code(self):
        code = self.cleaned_data['code']
       
        if code == 'generate':
            pref = datetime.datetime.now().strftime('%y%m%d')
            code = 1
            while True:
                try:
                    check = models.Laundry.objects.get(code = f"{pref}{code:05d}")
                    code = code + 1
                except:
                    return f"{pref}{code:05d}"
                    break
        else:
            return code
    
    def clean_payment(self):
        tendered = float(self.data['tendered'])
        if tendered > 0:
            return 1
        else:
            return 0

    def save(self):
        instance = self.instance
        Products = []
        Items = []
        Coupons = []
        # print(f"{self.data}")
        if 'price_id[]' in self.data:
            for k, val in enumerate(self.data.getlist('price_id[]')):
                prices = models.Prices.objects.get(id= val)
                price = self.data.getlist('laundry_price[]')[k]
                weight = self.data.getlist('laundry_weight[]')[k]
                total = float(price) * float(weight)
                try:
                    Items.append(models.LaundryItems(laundry = instance, laundry_type = prices,category=prices,category_type=prices,user_type=prices, price = price,weight = weight, total_amount = total))
                    print("LaundryItems..")
                except Exception as err:
                    print(err)
                    return False
        try:
            instance.save()
            models.LaundryItems.objects.filter(laundry = instance).delete()
            models.LaundryItems.objects.bulk_create(Items)
        except Exception as err:
            print(err)
            return False
        if 'coupon_id[]' in self.data:
            for k, val in enumerate(self.data.getlist('coupon_id[]')):
                coupon = models.Coupon.objects.get(id= val)
                discount_type = self.data.getlist('coupon_discount_type[]')[k]
                discount = self.data.getlist('coupon_discount[]')[k]
                
                try:
                    laundry_item = models.LaundryItems.objects.get(laundry=instance)
                    total_amount = laundry_item.total_amount
                except models.LaundryItems.DoesNotExist:
                    total_amount = 0
                
                if discount_type == '1':  # Percentage discount
                    discount = (total_amount * float(discount)) / 100  # Convert discount to float
                elif discount_type == '2':  # Fixed amount discount
                    discount = float(discount)  # Convert discount to float

                total = total_amount - discount  # Now subtraction should work

                print(total)
                
                try:
                    Coupons.append(models.LaundryCoupons(laundry = instance, coupon = coupon, discount_type = discount_type, discount = discount, total_amount = total))
                    print("Laundrycoupons..")
                except Exception as err:
                    print(err)
                    return False
        try:
            instance.save()
            models.LaundryCoupons.objects.filter(laundry = instance).delete()
            models.LaundryCoupons.objects.bulk_create(Coupons)
          
        except Exception as err:
            print(err)
            return False

            raise forms.ValidationError("Coupon is Invalid.")


class SaveLaundryVendor(forms.ModelForm):
    code = forms.CharField(max_length=250)
    # client = forms.CharField(max_length=250)
    contact = forms.CharField(max_length=250,required= False)
    status = forms.CharField(max_length=2)
    payment = forms.CharField(max_length=2)
    total_amount = forms.CharField(max_length=250)
    tendered = forms.CharField(max_length=250)
    pickup_date=forms.DateField()
    delivery_date=forms.DateField()
    Coupon_code=forms.CharField(max_length=20,required=False)
    mode = forms.CharField(max_length=20)
    barcode = forms.CharField(max_length=255, required=False )
    pickup_time = forms.CharField(max_length=100)
    delivery_time = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)
    # franchise_details = forms.CharField(max_length=255)
    # vendor_details = forms.CharField(max_length=255)
    pincode = forms.IntegerField()

    class Meta:
        model = models.Laundry
        fields = ('code', 'client', 'contact', 'status', 'payment', 'total_amount', 'tendered','pickup_date','delivery_date','Coupon_code','mode','barcode','pickup_time','delivery_time','address','pincode','franchise_details', 'vendor_details')

    def clean_code(self):
        code = self.cleaned_data['code']
       
        if code == 'generate':
            pref = datetime.datetime.now().strftime('%y%m%d')
            code = 1
            while True:
                try:
                    check = models.Laundry.objects.get(code = f"{pref}{code:05d}")
                    code = code + 1
                except:
                    return f"{pref}{code:05d}"
                    break
        else:
            return code
    
    def clean_payment(self):
        tendered = float(self.data['tendered'])
        if tendered > 0:
            return 1
        else:
            return 0

    def save(self):
        instance = self.instance
        Products = []
        Items = []
        Coupons = []
        # print(f"{self.data}")
        if 'price_id[]' in self.data:
            for k, val in enumerate(self.data.getlist('price_id[]')):
                prices = models.Prices.objects.get(id= val)
                price = self.data.getlist('laundry_price[]')[k]
                weight = self.data.getlist('laundry_weight[]')[k]
                total = float(price) * float(weight)
                try:
                    Items.append(models.LaundryItems(laundry = instance, laundry_type = prices,category=prices,category_type=prices,user_type=prices, price = price,weight = weight, total_amount = total))
                    print("LaundryItems..")
                except Exception as err:
                    print(err)
                    return False
        try:
            instance.save()
            models.LaundryItems.objects.filter(laundry = instance).delete()
            models.LaundryItems.objects.bulk_create(Items)
        except Exception as err:
            print(err)
            return False
        if 'coupon_id[]' in self.data:
            for k, val in enumerate(self.data.getlist('coupon_id[]')):
                coupon = models.Coupon.objects.get(id= val)
                discount_type = self.data.getlist('coupon_discount_type[]')[k]
                discount = self.data.getlist('coupon_discount[]')[k]
                
                try:
                    laundry_item = models.LaundryItems.objects.get(laundry=instance)
                    total_amount = laundry_item.total_amount
                except models.LaundryItems.DoesNotExist:
                    total_amount = 0
                
                if discount_type == '1':  # Percentage discount
                    discount = (total_amount * float(discount)) / 100  # Convert discount to float
                elif discount_type == '2':  # Fixed amount discount
                    discount = float(discount)  # Convert discount to float

                total = total_amount - discount  # Now subtraction should work

                print(total)
                
                try:
                    Coupons.append(models.LaundryCoupons(laundry = instance, coupon = coupon, discount_type = discount_type, discount = discount, total_amount = total))
                    print("Laundrycoupons..")
                except Exception as err:
                    print(err)
                    return False
        try:
            instance.save()
            models.LaundryCoupons.objects.filter(laundry = instance).delete()
            models.LaundryCoupons.objects.bulk_create(Coupons)
          
        except Exception as err:
            print(err)
            return False

            raise forms.ValidationError("Coupon is Invalid.")

# # tickets
# class TicketsForm(forms.ModelForm):
#     class Meta:
#         model=Tickets
#         fields=('Franchise_branch','Customer_ID','Title','image','Type_of_Tickets','Description')


# class statusupdate(forms.ModelForm):
#     class Meta:
#         model=Tickets
#         fields=('status',)  
#         help_texts = {
#             'status': None,
          
#         } 

# tickets
class TicketsForm(forms.ModelForm):
    class Meta:
        model=Tickets
        fields=('Franchise_branch','Customer_ID','Title','image','Type_of_Tickets','Description')
        labels = {
            'Franchise_branch': 'Franchise Branch',
            'Customer_ID': 'Customer ID',
            'Title': 'Title',
            'image': 'Image',
            'Type_of_Tickets': 'Type of Tickets',
            'Description': 'Description',
        }

class statusupdate(forms.ModelForm):
    class Meta:
        model=Tickets
        fields=('status',)  
        help_texts = {
            'status': None,
          
        } 

class Savestaffs(forms.ModelForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    # password1 = forms.CharField(max_length=250)
    # password2 = forms.CharField(max_length=250)
    # is_staff = forms.BooleanField(initial=False)
    class Meta:
        model = Staffs
        fields = ('email', 'username','first_name', 'last_name', 'designation', 'district', 'location', 'city', 'phone', 'franchise_details','photo','aadhar','pan_card')

class Updatestaffs(forms.ModelForm):
    # username = forms.CharField(max_length=250,help_text="The Username field is required.")
    # email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    # first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    # last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")

    class Meta:
        model = Staffs
        fields = ('email', 'username', 'first_name', 'last_name', 'designation', 'district', 'location', 'city', 'phone', 'franchise_details','photo','aadhar','pan_card')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = Staffs.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = Staffs.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")


CHART_CHOICES = (
    ('#1','Bar Chart'),
    ('#2','Pie Chart'),
    ('#3','Line Chart'),
)
RESULT_CHOICES =(
    ('#1','transaction'),
    ('#2','sales date'),
    # ('#3','Cutomers'),
    

)
class SalesSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)
    results_by = forms.ChoiceField(choices=RESULT_CHOICES)

class SuperSalesSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)
    results_by = forms.ChoiceField(choices=RESULT_CHOICES)
    franchise_details = forms.CharField(max_length=250)
    
class SaveCoupon(forms.ModelForm):
    code = forms.CharField(max_length=250)
    discount= forms.CharField(max_length=20)
    user_limit= forms.CharField(max_length=20)
    valid_from = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    valid_to = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    status = forms.CharField(max_length=2)
    discount_type = forms.CharField(max_length=2)
    
    class Meta:
        model = models.Coupon
        fields = ('code', 'discount','user_limit', 'valid_from','valid_to', 'status', 'discount_type')

class SaveCouponFranchise(forms.ModelForm):
    code = forms.CharField(max_length=250)
    discount= forms.CharField(max_length=20)
    user_limit= forms.CharField(max_length=20)
    valid_from = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    valid_to = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    status = forms.CharField(max_length=2)
    discount_type = forms.CharField(max_length=2)
    
    class Meta:
        model = models.Coupon
        fields = ('code', 'discount','user_limit', 'valid_from','valid_to', 'status', 'discount_type','franchise_details')

class UpdateCoupon(forms.Form):
    code = forms.CharField(max_length=250)
    discount= forms.CharField(max_length=20)
    user_limit= forms.CharField(max_length=20)
    valid_from = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    valid_to = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    status = forms.CharField(max_length=2)
    discount_type = forms.CharField(max_length=2)
    
    class Meta:
        model = models.Coupon
        fields = ('code', 'discount','user_limit', 'valid_from','valid_to', 'status', 'discount_type')

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            coupon =Coupon.objects.exclude(id=self.cleaned_data['id']).get(code = code)
        except Exception as e:
            return code
        raise forms.ValidationError(f"The {coupon.code} code is already exists/taken")

class SaveBanner(forms.ModelForm):
    banner_type= forms.CharField(max_length=250)
    title= forms.CharField(max_length=20)
    status = forms.CharField(max_length=2)
    description = forms.CharField(max_length=200)
    
    class Meta:
        model = models.Banners
        fields = ('banner_type', 'title','image', 'description')

class UpdateBanner(forms.Form):
    banner_type= forms.CharField(max_length=250)
    title= forms.CharField(max_length=20)
    status = forms.CharField(max_length=2)
    description = forms.CharField(max_length=2)
    
    class Meta:
        model = Banners
        fields = ('banner_type', 'title','image', 'description')

class SaveContact(forms.ModelForm):
    Address= forms.CharField(max_length=250)
    phone= forms.CharField(max_length=20)
    alternative_phone = forms.CharField(max_length=20)
    email_1 = forms.CharField(max_length=200)
    email_2 = forms.CharField(max_length=200)
    
    class Meta:
        model = models.Contact
        fields = ('Address', 'email_1','email_2', 'phone', 'alternative_phone')


class SaveTerms(forms.ModelForm):
    description= forms.CharField(max_length=2000)   
    class Meta:
        model = models.TermsCondition
        fields = ('description', )

class SaveAbout(forms.ModelForm):
    description= forms.CharField(max_length=2000)   
    class Meta:
        model = models.AboutUs
        fields = ('description', )
