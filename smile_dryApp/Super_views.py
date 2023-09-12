from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, TicketsForm, statusupdate, SuperSalesSearchForm
import json
from django.contrib import messages
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import HttpResponse
from smile_dryApp import models, forms
from smile_dryApp.models import Customer, User, Tickets, Franchise_User, Vendor, Rider, Staffs, Laundry, chatMessages, CCTV, Coupon, Banners, Products, Contact, Notification, Franchise_Notification
from django.db.models import Q, Sum
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse
import pandas as pd
from .utils import get_chart
from datetime import datetime
from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from . import models, forms
from django.utils.safestring import mark_safe
from decimal import Decimal
# Create your views here.

def context_data(request):
    fullpath = request.get_full_path()
    abs_uri = request.build_absolute_uri()
    abs_uri = abs_uri.split(fullpath)[0]
    context = {
        'system_host' : abs_uri,
        'page_name' : '',
        'page_title' : '',
        'system_name' : 'Smiley Dry',
        'system_short_name' : 'SD',
        'topbar' : True,
        'footer' : True,
    }
    return context



def admin(request):
    customer_count = Customer.objects.filter(is_customer=True).count()
    
    
    tickets_count = Tickets.objects.all().count()
    date = datetime.now()
    year = date.strftime('%Y')
    month = date.strftime('%m')
    day = date.strftime('%d')
    today_orders = models.Laundry.objects.filter(
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
    ).count()
    todays_sales = models.Laundry.objects.filter(
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
    ).aggregate(Sum('total_amount'))['total_amount__sum']
    pending_orders = models.Laundry.objects.filter(status= 0).count()
    processing_orders = models.Laundry.objects.filter(status= 1).count()
    delivered_orders = models.Laundry.objects.filter(status= 2).count()
    labels = []
    data = []        
    # queryset = models.Laundry.objects.values('franchise_details').annotate(total_sales=Sum('total_amount')).order_by('franchise_details')
    # for item in queryset:
    #     labels.append(item['franchise_details'])  # Use item['franchise_details'] instead of item.franchise_details
    #     data.append(item['total_sales'])
    context = {
        'customer_count': customer_count,
        'tickets_count': tickets_count,
        'todays_sales': todays_sales,
        'today_orders': today_orders,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'delivered_orders': delivered_orders,
        'labels'    : labels,
        'data'      : data,
    }
    context['laundries'] = models.Laundry.objects.order_by('-date_added')[:5]  # Retrieve only the first 10 objects
    # # Calculate total daily sales for each franchise
    franchises = models.Laundry.objects.values('franchise_details').annotate(total_sales=Sum('total_amount')).order_by('franchise_details')
    
    franchise_labels = [franchise['franchise_details'] for franchise in franchises]
    franchise_sales = [franchise['total_sales'] for franchise in franchises]

    context['labels'] = franchise_labels
    context['data'] = franchise_sales

    return render(request, 'Super_admin_templates/admin_dashboard_card_link.html', context)
    
def admin_dashboard(request):
    date = datetime.now()
    year = date.strftime('%Y')
    month = date.strftime('%m')
    day = date.strftime('%d')
    today_orders = models.Laundry.objects.filter(
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
    ).count()
    todays_sales = models.Laundry.objects.filter(
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
    ).aggregate(Sum('total_amount'))['total_amount__sum']
    pending_orders = models.Laundry.objects.filter(status= 0).count()
    delivered_orders = models.Laundry.objects.filter(status= 2).count()
    return render(request, 'Super_admin_templates/admin_dashboard_card_link.html',{'franchise_customer_count' : franchise_customer_count, 'tickets_count_franchise' : tickets_count_franchise, 'todays_sales' : todays_sales, 
                                                                                        'today_orders': today_orders, 'pending_orders': pending_orders, 'delivered_orders': delivered_orders, 'users': users })
    

def customer(request):
    return render(request,'Super_admin_templates/admin.html')

def vendor(request):
    return render(request,'Super_admin_templates/admin.html')

def rider(request):
    return render(request,'Super_admin_templates/admin.html')


def update_profile(request):
    context = context_data(request)
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id = request.user.id)
    if not request.method == 'POST':
        form = forms.UpdateProfile(instance=user)
        context['form'] = form
        print(form)
    else:
        form = forms.UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile-page")
        else:
            context['form'] = form
            
    return render(request, 'Super_admin_templates/manage_profile.html',context)

@login_required
def update_password(request):
    context =context_data(request)
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = forms.UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile-page")
        else:
            context['form'] = form
    else:
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'Super_admin_templates/update_password.html',context)

@login_required
def profile(request):
    context = context_data(request)
    context['page'] = 'profile'
    context['page_title'] = "Profile"
    return render(request,'Super_admin_templates/profile.html', context)

def logout_user(request):
    logout(request)
    return redirect('login-page')

@login_required
def users(request):
    context = context_data(request)
    context['page'] = 'users'
    context['page_title'] = "User List"
    context['users'] = Customer.objects.filter(is_customer=True)
    return render(request, 'Super_admin_templates/users.html', context)

@login_required
def save_user(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            user = Customer.objects.get(id = post['id'], is_customer=True)
            form = forms.UpdateUser(request.POST, instance=user)
        else:
            form = forms.SaveUser(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Customer has been saved successfully.")
            else:
                messages.success(request, "Customer has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def manage_user(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_user'
    context['page_title'] = 'Manage User'
    context['fusers'] = models.User.objects.filter(is_franchise = True).all()
    if pk is None:
        context['user'] = {}
    else:
        context['user'] = Customer.objects.get(id=pk)
    
    return render(request, 'Super_admin_templates/manage_user.html', context)

@login_required
def delete_user(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'User ID is invalid'
    else:
        try:
            Customer.objects.filter(pk = pk).delete()
            messages.success(request, "Customer has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Customer Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_user(request, pk=None):
    context = context_data(request)
    context['page'] = 'view_user'
    context['page_title'] = 'View user'

    if pk is None:
        context['user'] = {}
        
    else:
        context['user'] = models.Customer.objects.get(id=pk)

    # if context['user']:
    #     user_name = context['user'].username
    #     context['laundries'] = models.Laundry.objects.filter(client=user_name).order_by('-date_added')[:5]
    # else:
    #     context['laundries'] = []
    user_name = context['user'].username
    print(user_name)
    context['laundries'] = models.Laundry.objects.filter(client=user_name).order_by('-date_added')[:5]
    return render(request, 'Super_admin_templates/view_user.html', context)


@login_required
def franchise(request):
    context = context_data(request)
    context['page'] = 'franchise'
    context['page_title'] = "Franchise List"
    context['users'] = User.objects.filter(is_franchise=True)
    return render(request, 'Super_admin_templates/franchise.html', context)

@login_required
def save_franchise(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            user = User.objects.get(id = post['id'], is_franchise=True)
            form = forms.Updatefranchise(request.POST, instance=user)
        else:
            form = forms.Savefranchise(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Franchise has been saved successfully.")
            else:
                messages.success(request, "Franchise has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def manage_franchise(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_franchise'
    context['page_title'] = 'Manage franchise'
    if pk is None:
        context['user'] = {}
    else:
        context['user'] = User.objects.get(id=pk)
    
    return render(request, 'Super_admin_templates/manage_franchise.html', context)

@login_required
def update_password_franchise(request, pk=None):
    context = context_data(request)
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        user = User.objects.get(id=pk)
        form = forms.UpdatePasswords(user = user, data= request.POST)
        context['user']=user
        if form.is_valid():
            form.save()
            messages.success(request,"Franchise Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("franchise-page")
        else:
            context['form'] = form
    else:
        user = User.objects.get(id=pk)
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
        context['user']=user
       
    return render(request,'Super_admin_templates/update_password _franchise.html',context)

@login_required
def delete_franchise(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'User ID is invalid'
    else:
        try:
            User.objects.filter(pk = pk).delete()
            messages.success(request, "Franchise has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Franchise Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_franchise(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_franchise'
    context['page_title'] = 'View Franchise'
    if pk is None:
        context['user'] = {}
        
    else:
        context['user'] = models.User.objects.get(id=pk)
        
    
    return render(request, 'Super_admin_templates/view_franchise.html', context)

@login_required
def update_status(request, pk = None):
    context = context_data(request)
    context['page'] = 'update_laundry'
    context['page_title'] = 'Update Transaction'
    if pk is None:
        context['users'] = {}
    else:
        context['users'] = models.User.objects.get(id=pk)
    print(pk)
    return render(request, 'Super_admin_templates/update_status.html', context)

@login_required
def update_user_status(request):
    resp = { 'status' : 'failed', 'msg':''}
    if request.POST['id'] is None:
        resp['msg'] = 'User ID is invalid'
    else:
        try:
            User.objects.filter(pk = request.POST['id']).update(status = request.POST['status'])
            messages.success(request, "User Status has been updated successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Updation Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def vendor(request):
    context = context_data(request)
    context['page'] = 'vendor'
    context['page_title'] = "Vendors List"
    context['users'] =  User.objects.filter(is_vendor=True)
    return render(request, 'Super_admin_templates/vendor.html', context)

@login_required
def save_vendor(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            user = User.objects.get(id = post['id'], is_vendor=True)
            form = forms.Updatevendor(request.POST, instance=user)
        else:
            form = forms.Savevendor(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Vendor has been saved successfully.")
            else:
                messages.success(request, "Vendor has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def manage_vendor(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_vendor'
    context['page_title'] = 'Manage vendor'
    context['fusers'] = models.User.objects.filter(is_franchise = True).all()
    if pk is None:
        context['user'] = {}
    else:
        context['user'] = Vendor.objects.get(id=pk)
    
    return render(request, 'Super_admin_templates/manage_vendor.html', context)

@login_required
def delete_vendor(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'User ID is invalid'
    else:
        try:
            User.objects.filter(pk = pk).delete()
            messages.success(request, "Vendor has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Vendor Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_vendor(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_vendor'
    context['page_title'] = 'View Vendor'
    if pk is None:
        context['user'] = {}
        
    else:
        context['user'] = models.User.objects.get(id=pk)
        
    
    return render(request, 'Super_admin_templates/view_vendor.html', context)


def update_password_vendor(request, pk=None):
    context = context_data(request)
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        user = User.objects.get(id=pk)
        form = forms.UpdatePasswords(user = user, data= request.POST)
        context['user']=user
        if form.is_valid():
            form.save()
            messages.success(request,"Vendor Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("vendor-page")
        else:
            context['form'] = form
    else:
        user = User.objects.get(id=pk)
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
        context['user']=user
       
       
    return render(request,'Super_admin_templates/update_password_vendor.html',context)

@login_required
def rider(request):
    context = context_data(request)
    context['page'] = 'rider'
    context['page_title'] = "Rider List"
    context['users'] =  User.objects.filter(is_rider=True)
    return render(request, 'Super_admin_templates/rider.html', context)

@login_required
def save_rider(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            user = User.objects.get(id = post['id'], is_rider=True)
            form = forms.Updaterider(request.POST, request.FILES, instance=user)
        else:
            form = forms.Saverider(request.POST,request.FILES) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Rider has been saved successfully.")
            else:
                messages.success(request, "Rider has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def manage_rider(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_rider'
    context['page_title'] = 'Manage rider'
    context['fusers'] = models.User.objects.filter(is_franchise = True).all()
    if pk is None:
        context['user'] = {}
    else:
        context['user'] = User.objects.get(id=pk)
    
    return render(request, 'Super_admin_templates/manage_rider.html', context)

@login_required
def delete_rider(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'User ID is invalid'
    else:
        try:
            User.objects.filter(pk = pk).delete()
            messages.success(request, "Rider has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Rider Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")
@login_required
def view_rider(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_rider'
    context['page_title'] = 'View rider'
    if pk is None:
        context['user'] = {}
        
    else:
        context['user'] = models.User.objects.get(id=pk)
        
    
    return render(request, 'Super_admin_templates/view_rider.html', context)


def update_password_rider(request, pk=None):
    context = context_data(request)
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        user = User.objects.get(id=pk)
        form = forms.UpdatePasswords(user = user, data= request.POST)
        context['user']=user
        if form.is_valid():
            form.save()
            messages.success(request,"Rider Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("rider-page")
        else:
            context['form'] = form
    else:
        user = User.objects.get(id=pk)
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
        context['user']=user
       
       
    return render(request,'Super_admin_templates/update_password_rider.html',context)


@login_required
def products(request):
    context = context_data(request)
    context['page'] = 'Product'
    context['page_title'] = "Product List"
    context['products'] = Products.objects.filter(delete_flag = 0).all()
    return render(request, 'Super_admin_templates/products.html', context)



@login_required
def save_product(request):
    resp = {'status': 'failed', 'msg': '', 'id': ''}
    
    if request.method == 'POST':
        post = request.POST
        GST = Decimal(post.get('GST'))  # Convert to Decimal
        sale_price = Decimal(post.get('sale_price'))  # Convert to Decimal
        purchase_rate = Decimal(post.get('purchase_rate'))
        if not post['id'] == '':
            price = sale_price + (sale_price * GST) / 100
            # print(price)
            total_purchase_rate = purchase_rate + (purchase_rate * GST) / 100
            print(total_purchase_rate)
            product = models.Products.objects.get(id=post['id'])
            form = forms.SaveProducts(request.POST, request.FILES, instance=product)
            product.price = price
            product.price = total_purchase_rate
        else:
            price = sale_price + (sale_price * GST) / 100
            # print(price)
            total_purchase_rate = purchase_rate + (purchase_rate * GST) / 100
            print(total_purchase_rate)
            form = forms.SaveProducts(request.POST, request.FILES)
            
        if form.is_valid():
            product = form.save(commit=False)
            product.price = price
            product.total_purchase_rate = total_purchase_rate
            product.save()
            
            if post['id'] == '':
                messages.success(request, "Product has been saved successfully.")
                pid = product.id
                resp['id'] = pid
            else:
                messages.success(request, "Product has been updated successfully.")
                resp['id'] = post['id']
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
        resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")





@login_required
def view_product(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_product'
    context['page_title'] = 'View Product'
    if pk is None:
        context['product'] = {}
        context['stockins'] = {}
    else:
        context['product'] = models.Products.objects.get(id=pk)
        context['stockins'] = models.StockIn.objects.filter(product__id=pk)
        context['stockouts'] = models.LaundryProducts.objects.filter(product__id=pk).order_by('productpurchase__code')
       
        stockin = models.StockIn.objects.filter(product__id = pk).aggregate(Sum('quantity'))
        context['stockin_count'] = stockin['quantity__sum']
        stockout = models.LaundryProducts.objects.filter(product__id = pk).aggregate(Sum('quantity'))
        context['stockout_count'] = stockout['quantity__sum']
    return render(request, 'Super_admin_templates/view_product.html', context)


@login_required
def manage_product(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_product'
    context['page_title'] = 'Manage product'
    
    if pk is None:
        context['product'] = {}
                
    else:
        context['product'] = models.Products.objects.get(id=pk)
    
    return render(request, 'Super_admin_templates/manage_product.html', context)

@login_required
def delete_product(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Product ID is invalid'
    else:
        try:
            models.Products.objects.filter(pk = pk).update(delete_flag = 1)
            messages.success(request, "Product has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Product Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def manage_productpurchase(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_product_invoice'
    context['page_title'] = 'Manage product_invoice'
    context['products'] = models.Products.objects.filter(delete_flag = 0, status = 1).all()
    context['fusers'] = models.User.objects.filter(is_franchise = True).all()
    # context['prices'] = models.Prices.objects.filter(delete_flag = 0, status = 1).all()
    if pk is None:
        context['productpurchase'] = {}
        # context['items'] = {}
        context['pitems'] = {}
    else:
        context['productpurchase'] = models.Productpurchase.objects.get(id=pk)
        # context['items'] = models.LaundryItems.objects.filter(laundry__id = pk).all()
        context['pitems'] = models.LaundryProducts.objects.filter(productpurchase__id = pk).all()
    
    return render(request, 'Super_admin_templates/manage_product_invoice.html', context)


def fetch_contact(request):
    if request.method == "GET":
        username = request.GET.get("username", "")
        try:
            user = User.objects.get(id=username)
            contact = user.phone if user.phone else ""
            return JsonResponse({"contact": contact})
        except User.DoesNotExist:
            return JsonResponse({"contact": ""})
    return JsonResponse({"contact": ""})
    
@login_required
def save_productpurchase(request):
    resp = { 'status': 'failed', 'msg' : '', 'id': '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            productpurchase = models.Productpurchase.objects.get(id = post['id'])
            form = forms.SaveProductpurchase(request.POST, instance=productpurchase)
        else:
            form = forms.SaveProductpurchase(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Invoice has been saved successfully.")
                pid = models.Productpurchase.objects.last().id
                resp['id'] = pid
            else:
                messages.success(request, "Invoice has been updated successfully.")
                resp['id'] = post['id']
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_productpurchase(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_productpurchase'
    context['page_title'] = 'View productpurchase'
    if pk is None:
        context['productpurchase'] = {}
        # context['items'] = {}
        context['pitems'] = {}
    else:
        context['productpurchase'] = models.Productpurchase.objects.get(id=pk)
        # context['items'] = models.Productpurchace.objects.filter(laundry__id = pk).all()
        context['pitems'] = models.LaundryProducts.objects.filter(productpurchase__id = pk).all()
    
    return render(request, 'Super_admin_templates/view_productpurchase.html', context)
@login_required
def delete_productpurchase(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Productpurchase ID is invalid'
    else:
        try:
            models.Productpurchase.objects.filter(pk = pk).delete()
            messages.success(request, "productpurchase has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting productpurchase Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def reciepts_productpurchase(request):
    context = context_data(request)
    context['page'] = 'reciepts'
    context['page_title'] = "reciepts List"
    # context['laundries'] = models.Laundry.objects.order_by('-date_added').all()
    context['productpurchases'] =  models.Productpurchase.objects.order_by('-date_added').all()
    # print(productpurchases)
    return render(request, 'Super_admin_templates/reciepts.html', context)

@login_required
def price(request):
    context = context_data(request)
    context['page'] = 'Price'
    context['page_title'] = "Price List"
    context['prices'] = models.Prices.objects.filter(delete_flag = 0).all()
    return render(request, 'Super_admin_templates/prices.html', context)

@login_required
def save_price(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            price = models.Prices.objects.get(id = post['id'])
            form = forms.SavePrice(request.POST, request.FILES, instance=price)
        else:
            form = forms.SavePrice(request.POST, request.FILES) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Categories has been saved successfully.")
            else:
                messages.success(request, "Categories has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_price(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_price'
    context['page_title'] = 'View Price'
    if pk is None:
        context['price'] = {}
    else:
        context['price'] = models.Prices.objects.get(id=pk)
    
    return render(request, 'Super_admin_templates/view_price.html', context)

@login_required
def manage_price(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_price'
    context['page_title'] = 'Manage price'
    if pk is None:
        context['price'] = {}
    else:
        context['price'] = models.Prices.objects.get(id=pk)
    
    return render(request, 'Super_admin_templates/manage_price.html', context)

@login_required
def delete_price(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Categories ID is invalid'
    else:
        try:
            models.Prices.objects.filter(pk = pk).update(delete_flag = 1)
            messages.success(request, "Categories has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Categories Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def update_status_prices(request, pk = None):
    context = context_data(request)
    context['page'] = 'update_price'
    context['page_title'] = 'Update Price'
    if pk is None:
        context['users'] = {}
    else:
        context['users'] = models.Prices.objects.get(id=pk)
    print(pk)
    return render(request, 'Super_admin_templates/update_status_prices.html', context)

@login_required
def update_prices_status(request):
    resp = { 'status' : 'failed', 'msg':''}
    if request.POST['id'] is None:
        resp['msg'] = 'ID is invalid'
    else:
        try:
            models.Prices.objects.filter(pk = request.POST['id']).update(status = request.POST['status'])
            messages.success(request, "Status has been updated successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Updation Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def staffs(request):
    context = context_data(request)
    context['page'] = 'staff'
    context['page_title'] = "Staff List"
    context['users'] =  Staffs.objects.filter(is_staff=True)
    return render(request, 'Super_admin_templates/staffs.html', context)

@login_required
def save_staffs(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            user = Staffs.objects.get(id = post['id'], is_staff=True)
            form = forms.Updatestaffs(request.POST, request.FILES, instance=user)
        else:
            form = forms.Savestaffs(request.POST, request.FILES) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Staff has been saved successfully.")
            else:
                messages.success(request, "Staff has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def manage_staffs(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_staff'
    context['page_title'] = 'Manage staff'
    context['fusers'] = models.User.objects.filter(is_franchise = True).all()
    if pk is None:
        context['user'] = {}
    else:
        context['user'] = Staffs.objects.get(id=pk)
    
    return render(request, 'Super_admin_templates/manage_staff.html', context)

@login_required
def delete_staffs(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Staff ID is invalid'
    else:
        try:
            Staffs.objects.filter(pk = pk).delete()
            messages.success(request, "Staff has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Staff Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_staffs(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_staff'
    context['page_title'] = 'View staff'
    if pk is None:
        context['user'] = {}
        
    else:
        context['user'] = models.Staffs.objects.get(id=pk)
        
    return render(request, 'Super_admin_templates/view_staff.html', context)    

@login_required
def manage_stockin(request,pid = None, pk = None):
    context = context_data(request)
    context['page'] = 'manage_stockin'
    context['page_title'] = 'Manage Stockin'
    context['pid'] = pid
    print(pid)
    print(pk)
    if pk is None:
        context['stockin'] = {}
    else:
        context['stockin'] = models.StockIn.objects.get(id=pk)
    
    return render(request, 'Super_admin_templates/manage_stockin.html', context)

@login_required
def save_stockin(request):
    resp = { 'status': 'failed', 'msg' : ''}
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            stockin = models.StockIn.objects.get(id = post['id'])
            form = forms.SaveStockIn(request.POST, instance=stockin)
        else:
            form = forms.SaveStockIn(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Stock Entry has been saved successfully.")
            else:
                messages.success(request, "Stock Entry has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_stockin(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Stock-in ID is invalid'
    else:
        try:
            models.StockIn.objects.filter(pk = pk).delete()
            messages.success(request, "Stock Entry Details has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Stock Entry Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def laundries(request):
    context = context_data(request)
    context['page'] = 'laundry'
    context['page_title'] = "laundry List"
    context['laundries'] = models.Laundry.objects.order_by('-date_added').all()
    return render(request, 'Super_admin_templates/laundries.html', context)

@login_required
def save_laundry(request):
    resp = { 'status': 'failed', 'msg' : '', 'id': '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            laundry = models.Laundry.objects.get(id = post['id'])
            form = forms.SaveLaundry(request.POST, instance=laundry)
        else:
            form = forms.SaveLaundry(request.POST) 
        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Laundry has been saved successfully.")
                pid = models.Laundry.objects.last().id
                resp['id'] = pid
            else:
                messages.success(request, "Laundry has been updated successfully.")
                resp['id'] = post['id']
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_laundry(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_laundry'
    context['page_title'] = 'View Laundry'
    if pk is None:
        context['laundry'] = {}
        context['items'] = {}
        context['pitems'] = {}
    else:
        context['laundry'] = models.Laundry.objects.get(id=pk)
        context['items'] = models.LaundryItems.objects.filter(laundry__id = pk).all()
        # context['pitems'] = models.LaundryProducts.objects.filter(laundry__id = pk).all()
    
    return render(request, 'Super_admin_templates/view_laundry.html', context)

@login_required
def manage_laundry(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_laundry'
    context['page_title'] = 'Manage laundry'
    context['products'] = models.Products.objects.filter(delete_flag = 0, status = 1).all()
    context['prices'] = models.Prices.objects.filter(delete_flag = 0, status = 1).all()
    if pk is None:
        context['laundry'] = {}
        context['items'] = {}
        context['pitems'] = {}
    else:
        context['laundry'] = models.Laundry.objects.get(id=pk)
        context['items'] = models.LaundryItems.objects.filter(laundry__id = pk).all()
        context['pitems'] = models.LaundryProducts.objects.filter(laundry__id = pk).all()
    
    return render(request, 'Super_admin_templates/manage_laundry.html', context)

@login_required
def delete_laundry(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Laundry ID is invalid'
    else:
        try:
            models.Laundry.objects.filter(pk = pk).delete()
            messages.success(request, "Laundry has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Laundry Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def update_status_laundry(request, pk = None):
    context = context_data(request)
    context['page'] = 'update_laundry'
    context['page_title'] = 'Update Transaction'
    if pk is None:
        context['laundry'] = {}
    else:
        context['laundry'] = models.Laundry.objects.get(id=pk)
    print(pk)
    return render(request, 'Super_admin_templates/update_status_laundry.html', context)

from django.contrib import messages
from .models import Notification

@login_required
def update_laundry_status_laundry(request):
    resp = {'status': 'failed', 'msg': ''}
    
    order_id = request.POST.get('id')  # Assuming you get the order ID from the form
    new_status = request.POST.get('status')  # Assuming you get the new status from the form

    if order_id is None:
        resp['msg'] = 'ID is invalid'
    else:
        try:
            # Update the order status
            laundry = models.Laundry.objects.filter(id=order_id).first()  # Retrieve the laundry record
            if laundry:
                laundry.status = new_status
                laundry.save()
            
                # Check if the new status is 'Cancelled'
                if new_status == '4':  # Assuming '4' represents the 'Cancelled' status
                    franchise = request.user  # Get the franchise user
                    heading = "Order Cancellation"
                    # code_link = f"<a href='{reverse('view-reciepts_franchise-pk', args=[laundry.id])}'>{laundry.code}</a>"
                    message = f"Your order with code {laundry.code} has been cancelled."
                    notification = Franchise_Notification.objects.create(sender=franchise, heading=heading, message=message)
            
                # messages.success(request, "Status has been updated successfully.")
                resp['status'] = 'success'
            else:
                resp['msg'] = "Laundry record not found"
        except:
            resp['msg'] = "Updation Failed"
    messages.success(request, "Status has been updated successfully.")
    return HttpResponse(json.dumps(resp), content_type="application/json")




# tickets
@login_required
def tickets(request):
  
    if request.method == 'POST':
           
        
        tickets_form=TicketsForm(request.POST, request.FILES)
        if tickets_form.is_valid():
            
          
               instance=tickets_form.save(commit=False)
               instance.user=request.user
        #        mail=request.user.email
        #        print(mail)
        #        send_mail('Hi Tickets has been Received', 'Thank you for letting us know of your concern, Have a Cookie while we explore into this matter.  Dont Reply to this mail', 'testerpython13@gmail.com', [mail],fail_silently=False)
               instance.save()
               
               messages.add_message(request,messages.SUCCESS, f'Your complaint has been registered!')
               return redirect('allcomplaints')
    else:
        
        tickets_form=TicketsForm(request.POST)
    context={'tickets_form':tickets_form,}
    context['fusers'] = models.User.objects.filter(is_franchise = True).all()
    return render(request,'Super_admin_templates/add_tickets.html',context)



@login_required
def list(request):
    c=Tickets.objects.filter(user=request.user).exclude(status='1')
    result=Tickets.objects.filter(user=request.user).exclude(Q(status='3') | Q(status='2'))
    c=Tickets.objects.all()
    args={'c':c,'result':result}
    return render(request,'Super_admin_templates/Complaints.html',args)

@login_required
def plist(request):
    result=Tickets.objects.filter(user=request.user).exclude(Q(status='1') | Q(status='3'))
    c=Tickets.objects.all()
    args={'result':result}
    return render(request,'Super_admin_templates/progresscomplaint.html',args)

@login_required
def allcomplaints(request):
      
        
        c=Tickets.objects.all().exclude(status='1')
        comp=request.GET.get("search")
        drop=request.GET.get("drop")

        if drop:
                c=c.filter(Q(Type_of_Tickets__icontains=drop))
        if comp:
                c=c.filter(Q(Type_of_Tickets__icontains=comp)|Q(Description__icontains=comp)|Q(Title__icontains=comp))
        if request.method=='POST':
                cid=request.POST.get('cid2')
                uid=request.POST.get('uid')
                print(uid)
                project = Tickets.objects.get(id=cid)
                
                forms=statusupdate(request.POST,instance=project)
                if forms.is_valid():
                        
                        obj=forms.save(commit=False)
                        mail = User.objects.filter(id=uid)
                        for i in mail:
                                m=i.email
                       
                      
                        print(m)
                        # send_mail('Hi, Tickets has been Resolved ', 'Thanks for letting us know of your concern, Hope we have solved your issue. Dont Reply to this mail', 'testerpython13@gmail.com', [m],fail_silently=False)
                        obj.save()
                        messages.add_message(request,messages.SUCCESS, f'The Tickets has been updated!')
                        return HttpResponseRedirect(reverse('allcomplaints'))
                else:
                        return render(request,'Super_admin_templates/AllComplaints.html')
                 #testing

        else:
                forms=statusupdate()
        # c=Complaint.objects.all().exclude(status='1')
           
        args={'c':c,'forms':forms,'comp':comp}
        return render(request,'Super_admin_templates/AllComplaints.html',args)
    
@login_required
def solved(request):
        
        cid=request.POST.get('cid2')
        c=Tickets.objects.all().exclude(Q(status='3') | Q(status='2'))
        comp=request.GET.get("search")
        drop=request.GET.get("drop")

        if drop:
                c=c.filter(Q(Type_of_Tickets__icontains=drop))
        if comp:
               
                c=c.filter(Q(Type_of_Tickets__icontains=comp)|Q(Description__icontains=comp)|Q(Title__icontains=comp))
        if request.method=='POST':
                cid=request.POST.get('cid2')
                print(cid)
                project = Tickets.objects.get(id=cid)
                forms=statusupdate(request.POST,instance=project)
                if forms.is_valid():
                        
                        obj=forms.save(commit=False)
                        obj.save()
                        messages.add_message(request,messages.SUCCESS, f'The Tickets has been updated!')
                        return HttpResponseRedirect(reverse('solved'))
                else:
                        return render(request,'Super_admin_templates/solved.html')
                 #testing

        else:
                forms=statusupdate()
        c=Tickets.objects.all().exclude(Q(status='3') | Q(status='2'))
        
        args={'c':c,'forms':forms,'comp':comp}
        return render(request,'Super_admin_templates/solved.html',args)  


def timeslot(request):

    timeslots = Timeslot.objects.all()

    context = {
        'timeslots': timeslots
    }

    return render(request, 'Super_admin_templates/timeslot.html', context)
@login_required
def daily_report(request, date = None):
    context = context_data(request)
    context['page'] = 'view_laundry'
    context['page_title'] = 'Daily Transaction Report'
    
    if date is None :
        date = datetime.now()
        year = date.strftime('%Y')
        month = date.strftime('%m')
        day = date.strftime('%d')
    else:
        date =datetime.strptime(date, '%Y-%m-%d')
        year = date.strftime('%Y')
        month = date.strftime('%m')
        day = date.strftime('%d')

    context['date'] = date
    context['laundries'] = models.Laundry.objects.filter(
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
        )
    grand_total = 0
    for laundry in context['laundries']:
        grand_total += float(laundry.total_amount)
    context['grand_total'] = grand_total
    
    return render(request, 'Super_admin_templates/report.html', context)

@login_required
def report_view(request):
    sales_df =None
    merged_df =None
    positions_df = None
    df =None
    chart = None
    no_data = None
    search_form = SuperSalesSearchForm(request.POST or None)
    # report_form = ReportForm()
    if request.method =='POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')
        franchise_details = request.POST.get('franchise_details')

        
        sale_qs = Laundry.objects.filter(pickup_date__lte=date_to, pickup_date__gte=date_from, franchise_details= franchise_details)
        if len(sale_qs) >0:
            sales_df = pd.DataFrame(sale_qs.values())
            # sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            # sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['created'] = sales_df['pickup_date'].apply(lambda x: x.strftime("%b %d %Y, %I:%M %p")) 
            sales_df['updated'] = sales_df['delivery_date'].apply(lambda x: x.strftime("%b %d %Y, %I:%M %p"))            
            
            #sales_df['sales_id'] = sales_df['id']

            # positions_data =[]
            # for sale in sale_qs:
            #     for pos in sale.get_positions():
            #         obj ={
            #             'position_id': pos.id,
            #             'product': pos.product.name,
            #             'quantity': pos.quantity,
            #             'price':pos.price,
            #             'sales_id': pos.get_sales_id(),
            #             'chart': chart,
            #         }
            #         positions_data.append(obj)
            #print(sales_df['Created'],sales_df['updated'])
            print(sales_df,type(sales_df))
            
            # positions_df =pd.DataFrame((positions_data))  
            #merged_df = pd.merge(sales_df, positions_df,on='Sales ID' )    
            
            #= pd.DataFrame(qs.get_positions())


            chart = get_chart(chart_type, sales_df, results_by)
            #print("chart",chart)
            
            sales_df.rename({'code':'code', 'total_amount':'total_amount','created':'Created','updated':'Updated'},axis =1, inplace =True)
            sales_df = sales_df.to_html(index=False, justify='center').replace('<table border="1" class="dataframe">','<table class="table" style="text-align:center;">')
            #sales_df = sales_df.to_html(index=False).replace('<tr style="text-align: right;">','<tr style="text-align: center;">')

            # positions_df = positions_df.to_html()
            print(sales_df)
            #df = df.to_html()
            
            #print(sales_df)
            
            

        else:
            no_data = "No data available in this time frame."

    context={
        'search_form':search_form,
        # 'report_form':report_form,
        'sales_df': sales_df,
        'positions_df': positions_df,
        #'merged_df':merged_df,
        #'df':df,
        'chart':chart,
        'no_data': no_data,

    }
    context['fusers'] = models.User.objects.filter(is_franchise = True).all()
    return render(request, 'Super_admin_templates/report_generation.html',context)

# chat


# Create your views here.
@login_required
def chat_admin(request):
    # User = get_user_model()
    users = User.objects.filter(is_franchise=True).all()
    print(users)
    chats = {}
    if request.method == 'GET' and 'u' in request.GET:
        # chats = chatMessages.objects.filter(Q(user_from=request.user.id & user_to=request.GET['u']) | Q(user_from=request.GET['u'] & user_to=request.user.id))
        chats = chatMessages.objects.filter(Q(user_from=request.user.id, user_to=request.GET['u']) | Q(user_from=request.GET['u'], user_to=request.user.id))
        chats = chats.order_by('date_created')
    context = {
        "page":"chat_admin",
        "users":users,
        "chats":chats,
        "chat_id": int(request.GET['u'] if request.method == 'GET' and 'u' in request.GET else 0)
    }
    print(request.GET['u'] if request.method == 'GET' and 'u' in request.GET else 0)
    return render(request,"Super_admin_templates/chat.html",context)



def get_messages(request):
    chats = chatMessages.objects.filter(Q(id__gt=request.POST['last_id']),Q(user_from=request.user.id, user_to=request.POST['chat_id']) | Q(user_from=request.POST['chat_id'], user_to=request.user.id))
    new_msgs = []
    for chat in list(chats):
        data = {}
        data['id'] = chat.id
        data['user_from'] = chat.user_from.id
        data['user_to'] = chat.user_to.id
        data['message'] = chat.message
        data['date_created'] = chat.date_created.strftime("%b-%d-%Y %H:%M")
        print(data)
        new_msgs.append(data)
    return HttpResponse(json.dumps(new_msgs), content_type="application/json")

def send_chat(request):
    resp = {}
    # User = get_user_model()
    if request.method == 'POST':
        post =request.POST
        
        u_from = User.objects.get(id=post['user_from'])
        u_to = User.objects.get(id=post['user_to'])
        insert = chatMessages(user_from=u_from,user_to=u_to,message=post['message'])
        try:
            insert.save()
            resp['status'] = 'success'
        except Exception as ex:
            resp['status'] = 'failed'
            resp['mesg'] = ex
    else:
        resp['status'] = 'failed'

    return HttpResponse(json.dumps(resp), content_type="application/json")

# admin----live link ===CCTV  --->start
def CCTV_list(request):
    CCTVs = CCTV.objects.all()
    context = {'CCTVs': CCTVs}
    return render(request, 'Super_admin_templates/CCTV_list.html', context)

def CCTV_delete(request,tid):
    y=CCTV.objects.get(Franchise_name=tid)
    y.delete()
    return redirect('CCTV_list')

# admin----live link ===CCTV  --->end


#Banners
@login_required
def coupon(request):
    context = context_data(request)
    context['page'] = 'Coupon'
    context['page_title'] = "Coupon List"
    context['coupons'] =  Coupon.objects.all()
    return render(request, 'Super_admin_templates/coupon_code.html', context)


@login_required
def manage_coupon(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_coupon'
    context['page_title'] = 'Manage coupon'
    if pk is None:
        context['coupon'] = {}
    else:
        context['coupon'] = Coupon.objects.get(id=pk)
    
    return render(request, 'Super_admin_templates/manage_coupon.html', context)

@login_required
def save_coupon(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            coupon = Coupon.objects.get(id = post['id'])
            form = forms.SaveCoupon(request.POST, instance=coupon)
        else:
            form = forms.SaveCoupon(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Coupon has been saved successfully.")
            else:
                messages.success(request, "Coupon has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_coupon(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'coupon ID is invalid'
    else:
        try:
            Coupon.objects.filter(pk = pk).delete()
            messages.success(request, "Coupon has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Coupon Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_coupon(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_coupon'
    context['page_title'] = 'View coupon'
    if pk is None:
        context['coupon'] = {}
        
    else:
        context['coupon'] = Coupon.objects.get(id=pk)
        
    
    return render(request, 'Super_admin_templates/view_coupon.html', context)
@login_required
def apply_coupon_page(request):
    context = context_data(request)
    context['page'] = 'Coupon'
    context['page_title'] = "Coupon List"
    context['coupons'] =  Coupon.objects.all()
    return render(request, 'Super_admin_templates/coupon_apply.html', context)

from django.shortcuts import render
from django.http import JsonResponse
from .models import Coupon
from datetime import date
def apply_coupon(request):
    if request.method == "POST":
        price = float(request.POST.get("price"))
        coupon_code = request.POST.get("coupon_code")
        print(coupon_code)
        try:
            coupon = Coupon.objects.get(code=coupon_code, valid_from__lte=date.today(), valid_to__gte=date.today(), status='1')
        except Coupon.DoesNotExist:
            coupon = None
        
        discount_amount = 0
        print(coupon.discount)
        if coupon:
            if coupon.discount_type == '1':  # Percentage discount
                discount_amount = (price * coupon.discount) / 100
            elif coupon.discount_type == '2':  # Fixed amount discount
                discount_amount = coupon.discount
        
        total_amount = price - discount_amount
        
        response_data = {
            "status": "success",
            "message": "Coupon applied successfully.",
            "discount_amount": discount_amount,
            "total_amount": total_amount,
        }
        print(discount_amount)
        print(total_amount)
        return JsonResponse(response_data)
    
    return JsonResponse({"status": "error", "message": "Invalid request method."})



#Banners
@login_required
def banner_page(request):
    context = context_data(request)
    context['page'] = 'banner'
    context['page_title'] = "banner List"
    context['Banners'] =  Banners.objects.all()
    return render(request, 'Super_admin_templates/banners.html', context)


@login_required
def manage_banner(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_banner'
    context['page_title'] = 'Manage banner'
    if pk is None:
        context['banner'] = {}
    else:
        context['banner'] = Banners.objects.get(id=pk)
    
    return render(request, 'Super_admin_templates/manage_banner.html', context)

@login_required
def save_banner(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            banners = Banners.objects.get(id = post['id'])
            form = forms.SaveBanner(request.POST, request.FILES, instance=banners)
        else:
            form = forms.SaveBanner(request.POST, request.FILES) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Banner has been saved successfully.")
            else:
                messages.success(request, "Banner has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_banner(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'banner ID is invalid'
    else:
        try:
            Banners.objects.filter(pk = pk).delete()
            messages.success(request, "Banner has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Banner Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_banner(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_banner'
    context['page_title'] = 'View banner'
    if pk is None:
        context['banner'] = {}
        
    else:
        context['banner'] = Banners.objects.get(id=pk)
        
    
    return render(request, 'Super_admin_templates/view_banner.html', context)



#Contact
@login_required
def contact(request):
    context = context_data(request)
    context['page'] = 'contact'
    context['page_title'] = "contact List"
    context['contacts'] =  Contact.objects.all()
    return render(request, 'Super_admin_templates/contact.html', context)


@login_required
def manage_contact(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_contact'
    context['page_title'] = 'Manage contact'
    if pk is None:
        context['contact'] = {}
    else:
        context['contact'] = Contact.objects.get(id=pk)
    
    return render(request, 'Super_admin_templates/manage_contact.html', context)

@login_required
def save_contact(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            contacts = Contact.objects.get(id = post['id'])
            form = forms.SaveContact(request.POST, instance=contacts)
        else:
            form = forms.SaveContact(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Contact has been saved successfully.")
            else:
                messages.success(request, "Contact has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def terms_conditions(request):
    context = context_data(request)
    context['page'] = 'users'
    context['page_title'] = "User List"
    context['terms'] =  models.TermsCondition.objects.all()
    # for term in context['terms']:
    #     term.description = mark_safe(term.description)
    print(id)
    return render(request, 'Super_admin_templates/T&C.html', context)

@login_required
def save_terms_conditions(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            terms = models.TermsCondition.objects.get(id = post['id'])
            form = forms.SaveTerms(request.POST, instance=terms)
        else:
            form = forms.SaveTerms(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "T&C has been saved successfully.")
            else:
                messages.success(request, "T&C has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def manage_terms_conditions(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_terms'
    context['page_title'] = 'Manage terms'
    if pk is None:
        context['terms'] = {}
    else:
        context['terms'] = models.TermsCondition.objects.get(id=pk)
    
    return render(request, 'Super_admin_templates/manage_T&C.html', context)

@login_required
def about_us(request):
    context = context_data(request)
    context['page'] = 'About Us'
    context['page_title'] = "About_Us"
    context['about_us'] =  models.AboutUs.objects.all()
    return render(request, 'Super_admin_templates/about_us.html', context)

@login_required
def save_about_us(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            about_us = models.AboutUs.objects.get(id = post['id'])
            form = forms.SaveAbout(request.POST, instance = about_us)
        else:
            form = forms.SaveAbout(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "About Us has been saved successfully.")
            else:
                messages.success(request, "About Us has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def manage_about_us(request, pk = None):
    context = context_data(request)
    context['page'] = 'about_us'
    context['page_title'] = 'about_us'
    if pk is None:
        context['about_us'] = {}
    else:
        context['about_us'] = models.AboutUs.objects.get(id=pk)
    
    return render(request, 'Super_admin_templates/manage_about_us.html', context)



@login_required
def admin_notifications_view(request):
    notifications = Notification.objects.all().order_by('-created_at') # Get unread notifications
    return render(request, 'Super_admin_templates/inbox_notifications_list.html', {'notifications': notifications})



from django.shortcuts import get_object_or_404
@login_required
def inbox_convo(request, notification_id):
    print("Notification ID:", notification_id)
    # Retrieve the specific notification using the notification_id from the URL
    notification = get_object_or_404(Notification, id=notification_id)
    
    # Update the notification to mark it as read (assuming you want to do this)
    notification.is_read = True
    notification.save()
    
    # Query other unread notifications from the same sender
    # all_notifications = Notification.objects.filter(Q(sender=request.user) & Q(id=notification_id))
    all_notifications = Notification.objects.filter(id=notification_id)
    
    print("User ID:", request.user.id) 

    # return render(request, 'Super_admin_templates/app-inbox-conversation.html', {'notifications': unread_notifications})
    return render(request, 'Super_admin_templates/inbox_conversation.html', {'notifications': all_notifications})    


def mark_notification_read(request):
    if request.method == 'POST' and request.is_ajax():
        notification_id = request.POST.get('notification_id')
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.is_read = True
            notification.save()
            return JsonResponse({'status': 'success'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error'})


from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Timeslot

def timeslot(request):
    return render(request, 'Super_admin_templates/timeslot.html')

from django.core import serializers
from datetime import datetime, timedelta

def get_timeslots(request):
    opening_time = request.GET.get('opening_time')
    closing_time = request.GET.get('closing_time')
    selected_week_off = request.GET.get('selected_week_off')

    # Use the correct format string '%I:%M%p'
    start = datetime.strptime(opening_time, '%I:%M%p')
    end = datetime.strptime(closing_time, '%I:%M%p')

    timeslots = []
    current = start
    while current <= end - timedelta(hours=1):
        if current.strftime('%A').lower() != selected_week_off:
            timeslots.append({
                'start_time': current.strftime('%I:%M %p'),
                'end_time': (current + timedelta(hours=1)).strftime('%I:%M %p')
            })
        current += timedelta(hours=1)

    return JsonResponse({'timeslots': timeslots})




# def save_timeslots(request):
#     if request.method == 'POST':
#         timeslots_data = json.loads(request.body)
#         if timeslots_data:
#             try:
#                 for timeslot_data in timeslots_data:
#                     start_time, end_time = timeslot_data['timeslot'].split(' - ')
#                     day_of_week = timeslot_data['day_of_week']

#                     Timeslot.objects.create(
#                         start_time=start_time.strip(),
#                         end_time=end_time.strip(),
#                         day_of_week=day_of_week,
#                         status=timeslot_data['status']
#                     )
                
#                 return JsonResponse({'message': 'Timeslots saved successfully'}, status=200)
#             except Exception as e:
#                 return JsonResponse({'message': 'Error saving timeslots: ' + str(e)}, status=500)
#         else:
#             return JsonResponse({'message': 'No timeslots data provided'}, status=400)
#     else:
#         return JsonResponse({'message': 'Invalid request method'}, status=405)

def save_timeslots(request):
    if request.method == 'POST':
        timeslots_data = json.loads(request.body)
        print("Received timeslots data:", timeslots_data)  # Add this line
        if timeslots_data:
            try:
                for timeslot_data in timeslots_data:
                    start_time, end_time = timeslot_data['start_time'], timeslot_data['end_time']
                    day_of_week = timeslot_data['day_of_week']
                    status = timeslot_data['status']

                    # Create and save a Timeslot object
                    Timeslot.objects.create(
                        start_time=start_time,
                        end_time=end_time,
                        day_of_week=day_of_week,
                        status=status
                    )
                
                return JsonResponse({'message': 'Timeslots saved successfully'}, status=200)
            except Exception as e:
                return JsonResponse({'message': 'Error saving timeslots: ' + str(e)}, status=500)
        else:
            return JsonResponse({'message': 'No timeslots data provided'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

