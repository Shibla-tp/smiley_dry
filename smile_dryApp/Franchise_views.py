from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, TicketsForm, statusupdate, SalesSearchForm
import datetime
import json
from django.contrib import messages
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import HttpResponse
from smile_dryApp import models, forms
from smile_dryApp.models import User, Tickets, Customer, Vendor, Rider, Prices, Staffs, Attendance, Laundry, chatMessages, CCTV, Notification, FranchiseProducts, Franchise_Notification
from django.db.models import Q, Sum
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import B2C, pickup
from datetime import datetime
from django.http import JsonResponse
import base64
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import pandas as pd
from .utils import get_chart

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



def franchise(request):
    user = User.objects.get(id=request.user.id)
    franchise_customer_count = Customer.objects.filter(Q(is_customer=True) & Q(franchise_city= user)).count()
    
    
    tickets_count_franchise = Tickets.objects.filter(Franchise_branch= user).count()
    total_revenue = Tickets.objects.filter(Franchise_branch= user).count()
    date = datetime.now()
    year = date.strftime('%Y')
    month = date.strftime('%m')
    day = date.strftime('%d')
    today_orders = models.Laundry.objects.filter(
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
            franchise_details=user,
    ).count()
    todays_sales = models.Laundry.objects.filter(
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
            franchise_details=user,
    ).aggregate(Sum('total_amount'))['total_amount__sum']
    pending_orders = models.Laundry.objects.filter(Q(status= 0)&Q(franchise_details=user)).count()
    processing_orders = models.Laundry.objects.filter(Q(status= 1)&Q(franchise_details=user)).count()
    delivered_orders = models.Laundry.objects.filter(Q(status= 2)&Q(franchise_details=user)).count()
    laundry = models.Laundry.objects.filter(franchise_details=user).order_by('-code')
    labels = []
    data = [] 
    for item in laundry:
            labels.append(item.code)
            data.append(item.payment)
    context = {
        'franchise_customer_count': franchise_customer_count,
        'tickets_count_franchise': tickets_count_franchise,
        'todays_sales': todays_sales,
        'today_orders': today_orders,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'delivered_orders': delivered_orders,
        'labels'    : labels,
        'data'      : data,
    }
    context['laundries'] = models.Laundry.objects.filter(franchise_details=user).order_by('-date_added')[:5]  # Retrieve only the first 10 objects
    

    return render(request, 'Franchise_templates/franchise_dashboard_card_link.html', context)

# def admin(request):
#     return render(request,'Franchise_templates/admin_dashboard_card_link.html')

# def admin_dashboard(request):
#     customer_count = User.objects.all().count()
#     context = {
#         'customer_count': customer_count
#     }
#     return render(request,'Franchise_templates/admin_dashboard_card_link.html')
# @login_required
# def login_user_franchise(request):
#     context = context_data(request)
    
#     context['User'] = User.objects.get(id=request.user.id)
#     print(User)
#     return render(request,'Franchise_templates/franchise_dashboard_list', context)

@login_required
def profile_franchise(request):
    context = context_data(request)
    context['page'] = 'profile'
    context['page_title'] = "Profile"
    return render(request,'Franchise_templates/profile.html', context)

def update_profile_franchise(request):
    context = context_data(request)
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id = request.user.id)
    if not request.method == 'POST':
        form = forms.UpdateFranchiseProfile(instance=user)
        context['form'] = form
        print(form)
    else:
        form = forms.UpdateFranchiseProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile-page_franchise")
        else:
            context['form'] = form
            
    return render(request, 'Franchise_templates/manage_profile.html',context)

# @login_required
# def update_password(request):
#     context =context_data(request)
#     context['page_title'] = "Update Password"
#     if request.method == 'POST':
#         form = forms.UpdatePasswords(user = request.user, data= request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Your Account Password has been updated successfully")
#             update_session_auth_hash(request, form.user)
#             return redirect("profile-page")
#         else:
#             context['form'] = form
#     else:
#         form = forms.UpdatePasswords(request.POST)
#         context['form'] = form
#     return render(request,'Franchise_templates/update_password.html',context)

@login_required
def users_franchise(request):
    context = context_data(request)
    context['page'] = 'users'
    context['page_title'] = "User List"
    user = User.objects.get(id=request.user.id)
    context['users'] = Customer.objects.filter(Q(is_customer=True) & Q(franchise_city=user))
    return render(request, 'Franchise_templates/users.html', context)
    
@login_required
def save_user_franchise(request):
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
                messages.success(request, "User has been saved successfully.")
            else:
                messages.success(request, "User has been updated successfully.")
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
def manage_user_franchise(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_user'
    context['page_title'] = 'Manage User'
    context['fusers'] = models.User.objects.filter(is_franchise = True).all()
    if pk is None:
        context['users'] = {}
    else:
        context['users'] = Customer.objects.get(id=pk)
    
    return render(request, 'Franchise_templates/manage_user.html', context)

@login_required
def delete_user_franchise(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'User ID is invalid'
    else:
        try:
            Customer.objects.filter(pk = pk).delete()
            messages.success(request, "User has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting User Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_user_franchise(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_user'
    context['page_title'] = 'View user'
    if pk is None:
        context['users'] = {}
        
    else:
        context['users'] = models.Customer.objects.get(id=pk)
    user_name = context['users'].username
    print(user_name)
    user = User.objects.get(id=request.user.id)
    context['laundries'] = models.Laundry.objects.filter(client=user_name, franchise_details=user).order_by('-date_added')[:5]   
    
    return render(request, 'Franchise_templates/view_user.html', context)

@login_required
def vendor_franchise(request):
    context = context_data(request)
    context['page'] = 'vendor'
    context['page_title'] = "Vendors List"
    user = User.objects.get(id=request.user.id)
    context['users'] = User.objects.filter(Q(is_vendor=True) & Q(franchise_details=user))
    return render(request, 'Franchise_templates/vendor.html', context)

@login_required
def save_vendor_franchise(request):
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
                messages.success(request, "User has been saved successfully.")
            else:
                messages.success(request, "User has been updated successfully.")
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
def manage_vendor_franchise(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_vendor'
    context['page_title'] = 'Manage vendor'
    context['fusers'] = models.User.objects.filter(is_franchise = True).all()
    if pk is None:
        context['user'] = {}
    else:
        context['user'] = Vendor.objects.get(id=pk)
    
    return render(request, 'Franchise_templates/manage_vendor.html', context)
@login_required
def delete_vendor_franchise(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'User ID is invalid'
    else:
        try:
            User.objects.filter(pk = pk).delete()
            messages.success(request, "User has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting User Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_vendor_franchise(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_vendor'
    context['page_title'] = 'View Vendor'
    if pk is None:
        context['users'] = {}
        
    else:
        context['users'] = models.User.objects.get(id=pk)
        
    
    return render(request, 'Franchise_templates/view_vendor.html', context)


def update_password_vendor_franchise(request, pk=None):
    context = context_data(request)
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        user = User.objects.get(id=pk)
        form = forms.UpdatePasswords(user = user, data= request.POST)
        context['user']=user
        if form.is_valid():
            form.save()
            messages.success(request,"Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("vendor-page")
        else:
            context['form'] = form
    else:
        user = User.objects.get(id=pk)
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
        context['user']=user
       
       
    return render(request,'Franchise_templates/update_password_vendor.html',context)

@login_required
def rider_franchise(request):
    context = context_data(request)
    context['page'] = 'rider'
    context['page_title'] = "Rider List"
    user = User.objects.get(id=request.user.id)
    context['users'] = User.objects.filter(Q(is_rider=True) & Q(franchise_details=user))
    return render(request, 'Franchise_templates/rider.html', context)

@login_required
def save_rider_franchise(request):
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
def manage_rider_franchise(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_rider'
    context['page_title'] = 'Manage rider'
    context['fusers'] = models.User.objects.filter(is_franchise = True).all()
    if pk is None:
        context['user'] = {}
    else:
        context['user'] = Rider.objects.get(id=pk)
    
    return render(request, 'Franchise_templates/manage_rider.html', context)

@login_required
def delete_rider_franchise(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'User ID is invalid'
    else:
        try:
            Rider.objects.filter(pk = pk).delete()
            messages.success(request, "User has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting User Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_rider_franchise(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_rider'
    context['page_title'] = 'View rider'
    if pk is None:
        context['users'] = {}
        
    else:
        context['users'] = models.User.objects.get(id=pk)
        
    
    return render(request, 'Franchise_templates/view_rider.html', context)


def update_password_rider_franchise(request, pk=None):
    context = context_data(request)
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        user = User.objects.get(id=pk)
        form = forms.UpdatePasswords(user = user, data= request.POST)
        context['user']=user
        if form.is_valid():
            form.save()
            messages.success(request,"Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("rider-page")
        else:
            context['form'] = form
    else:
        user = User.objects.get(id=pk)
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
        context['user']=user
       
       
    return render(request,'Franchise_templates/update_password_rider.html',context)
@login_required
def price_franchise(request):
    context = context_data(request)
    context['page'] = 'Price'
    context['page_title'] = "Price List"
    context['prices'] = models.Prices.objects.filter(delete_flag = 0).all()
    return render(request, 'Franchise_templates/prices.html', context)
@login_required
def view_price_franchise(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_price'
    context['page_title'] = 'View Price'
    if pk is None:
        context['price'] = {}
    else:
        context['price'] = models.Prices.objects.get(id=pk)
    
    return render(request, 'Franchise_templates/view_price.html', context)

# walkin and pickup ====start
from datetime import datetime

def b2c_form(request):
    if request.method == 'GET':
        return render(request, 'Franchise_templates/b2c_form.html')
    elif request.method == 'POST':
        nm = request.POST.get('name', '')
        con = request.POST.get('contact', '')
        ser = request.POST.getlist('service')
        dd = request.POST.get('delivery-date', '')
        dt = request.POST.get('delivery-time', '')
        cc = request.POST.get('coupon', '')
        add = request.POST.get('address', '')

        # Validate date format
        try:
            delivery_date = datetime.strptime(dd, '%Y-%m-%d').date()
        except ValueError:
            # Handle invalid date format
            # Return an error message or redirect back to the form
            # You can also set a default value for `delivery_date` if needed
            return render(request, 'Franchise_templates/b2c_form.html', {'error': 'Invalid date format'})

        x = B2C.objects.create(customer_name=nm, contact_number=con, service=ser, delivery_date=delivery_date,
                               delivery_time=dt, Coupon_code=cc, address=add)
        x.save()
        return redirect('B2cview')

def B2cview(request):
    data=B2C.objects.all()
    return render(request,'Franchise_templates/b2c_view.html',{'data1':data})

# def manage_B2c(request,pk):
#     if request.method =="GET":
#         em=B2C.objects.get(id=pk)
#         return render(request,'manage_b2c.html',{'em1':em})

#     elif request.method=="POST":
#         nm = request.POST.get('name', '')
#         con = request.POST.get('contact', '')
#         ser = request.POST.getlist('service')
#         dd = request.POST.get('delivery-date', '')
#         dt = request.POST.get('delivery-time', '')
#         cc = request.POST.get('coupon', '')
#         add = request.POST.get('address', '')
#         a=B2C.objects.filter(id=pk).update(customer_name=nm, contact_number=con, service=ser, delivery_date=delivery_date,
#                                delivery_time=dt, Coupon_code=cc, address=add)
#         return redirect(B2cview)

def delete_B2c(request,pk):
    x=B2C.objects.get(id=pk)
    x.delete()
    return redirect(B2cview)





def pickup_form(request):
    if request.method == 'GET':
        return render(request, 'Franchise_templates/pickup_form.html')
    elif request.method == 'POST':
        nm = request.POST.get('name', '')
        con = request.POST.get('contact', '')
        pd = request.POST.get('pickup-date', '')
        pt = request.POST.get('pickup-time', '')
        ser = request.POST.getlist('service')
        dd = request.POST.get('delivery-date', '')
        dt = request.POST.get('delivery-time', '')
        cc = request.POST.get('coupon', '')
        est = request.POST.getlist('estimated')
        heavy = request.POST.getlist('heavy')
        add = request.POST.get('address', '')

        # Validate date format
        try:
            delivery_date = datetime.strptime(dd, '%Y-%m-%d').date()
            pickup_date = datetime.strptime(pd, '%Y-%m-%d').date()

        except ValueError:
            # Handle invalid date format
            # Return an error message or redirect back to the form
            # You can also set a default value for `delivery_date` if needed
            return render(request, 'Franchise_templates/pickup_form.html', {'error': 'Invalid date format'})

        x = pickup.objects.create(customer_name=nm, contact_number=con, service=ser, delivery_date=delivery_date,
                               delivery_time=dt,pickup_date=pd,pickup_time=pt, Coupon_code=cc,estimated_clothes_quantity=est,heavy_item=heavy, address=add)
        x.save()
        return redirect('pickupview')

def pickupview(request):
    data=pickup.objects.all()
    return render(request,'Franchise_templates/pickup_view.html',{'data1':data})

def delete_pickup(request,pk):
    x=pickup.objects.get(id=pk)
    x.delete()
    return redirect(pickupview)


# walkin and pickup ====end
@login_required
def staffs_franchise(request):
    context = context_data(request)
    context['page'] = 'staff'
    context['page_title'] = "Staff List"
    user = User.objects.get(id=request.user.id)
    context['users'] =  Staffs.objects.filter(Q(is_staff=True) & Q(franchise_details=user))
    return render(request, 'Franchise_templates/staffs.html', context)

@login_required
def save_staffs_franchise(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            user = Staffs.objects.get(id = post['id'], is_staff=True)
            form = forms.Updatestaffs(request.POST, request.FILES, instance=user)
        else:
            form = forms.Savestaffs(request.POST) 

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
def manage_staffs_franchise(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_staff'
    context['page_title'] = 'Manage staff'
    context['fusers'] = models.User.objects.filter(is_franchise = True).all()
    if pk is None:
        context['user'] = {}
    else:
        context['user'] = Staffs.objects.get(id=pk)
    
    return render(request, 'Franchise_templates/manage_staff.html', context)

@login_required
def delete_staffs_franchise(request, pk = None):
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
def view_staffs_franchise(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_staff'
    context['page_title'] = 'View staff'
    if pk is None:
        context['users'] = {}
        
    else:
        context['users'] = models.Staffs.objects.get(id=pk)
        
    return render(request, 'Franchise_templates/view_staff.html', context)  

# @login_required()
# def attendance_staff(request):
#     # now = timezone.now()
#     # # ass = get_object_or_404(Assign, id=assign_id)
#     # # att_list = ass.attendanceclass_set.filter(date__lte=now).order_by('-date')
#     # return render(request, 'Franchise_templates/t_class_date.html')
# @login_required
# def attendance_staff(request, date = None):
#     context = context_data(request)
#     context['page'] = 'view_laundry'
#     context['page_title'] = 'Daily Transaction Report'
    
#     if date is None:
#         date = dt.datetime.now()
#         year = date.strftime('%Y')
#         month = date.strftime('%m')
#         day = date.strftime('%d')
#     else:
#         date =dt.datetime.strptime(date, '%Y-%m-%d')
#         year = date.strftime('%Y')
#         month = date.strftime('%m')
#         day = date.strftime('%d')

#     context['date'] = date
#     context['laundries'] = models.Laundry.objects.filter(
#             date_added__year = year,
#             date_added__month = month,
#             date_added__day = day,
#         )
#     grand_total = 0
#     for laundry in context['laundries']:
#         grand_total += float(laundry.total_amount)
#     context['grand_total'] = grand_total
    
#     return render(request, 'Franchise_templates/attendance.html', context)

# # walkin and pickup ====start
# # from datetime import datetime

#Attendance
#     if request.method == 'POST':
#         post = request.POST
#         date = datetime.strptime(post['attendance_date'], '%Y-%m-%d')
#         year = date.strftime('%Y')
#         month = date.strftime('%m')
#         day = date.strftime('%d')
#         _class = Class.objects.get(id=post['classIns'])
#         Attendance.objects.filter(attendance_date__year = year, attendance_date__month = month, attendance_date__day = day,classIns = _class).delete()
#         for student in post.getlist('student[]'):
#             type = post['type['+student+']']
#             studInstance = Student.objects.get(id = student)
#             att = Attendance(student=studInstance,type = type,classIns = _class,attendance_date=post['attendance_date']).save()
#         resp['status'] = 'success'
#         messages.success(request,"Attendance has been saved successfully.")
#     return HttpResponse(json.dumps(resp),content_type="application/json")
#Attendance
@login_required
def attendance_class(request, date = None):
    # if request.user.profile.user_type == 1:
    #     classes = Class.objects.all()
    # else:
    #     classes = Class.objects.filter(assigned_faculty = request.user.profile).all()
    context = context_data(request)
    context['page'] = 'staff'
    # context['page_title'] = "Staff List"
    if not date is None:
        date = datetime.strptime(date, '%Y-%m-%d')
        year = date.strftime('%Y')
        month = date.strftime('%m')
        day = date.strftime('%d')
        attendance = Attendance.objects.filter(attendance_date__year = year, attendance_date__month = month, attendance_date__day = day).all()
    user = User.objects.get(id=request.user.id)
    context['users'] =  Staffs.objects.filter(Q(is_staff=True) & Q(franchise_details=user))
    context['page_title'] = "Attendance Management"
    # context['classes'] = classes
    return render(request, 'Franchise_templates/attendance_class.html',context)


# @login_required
# def attendance(request, date=None):
#     context = context_data(request)
#     context['page'] = 'staff'
#     # _class = Class.objects.get(id = classPK)
#     user = User.objects.get(id=request.user.id)
#     staffs = Staffs.objects.filter(Q(is_staff=True) & Q(franchise_details=user))
#     context['page_title'] = "Attendance Management"
#     # context['class'] = _class
#     context['date'] = date
#     att_data = {}
#     for staff in staffs:
#         att_data[staff.id] = {}
#         att_data[staff.id]['data'] = staff
#     if not date is None:
#         date = datetime.strptime(date, '%Y-%m-%d')
#         year = date.strftime('%Y')
#         month = date.strftime('%m')
#         day = date.strftime('%d')
#         attendance = Attendance.objects.filter(attendance_date__year = year, attendance_date__month = month, attendance_date__day = day).all()
#         for att in attendance:
#             att_data[att.staff.pk]['type'] = att.type
#     print(list(att_data.values()))
#     context['att_data'] = list(att_data.values())
#     context['staffs'] = staffs
#     return render(request, 'Franchise_templates/attendance_mgt.html',context)

# @login_required
# def save_attendance(request):
#     resp = {'status' : 'failed', 'msg':''}
#     if request.method == 'POST':
#         post = request.POST
#         date = datetime.strptime(post['attendance_date'], '%Y-%m-%d')
#         year = date.strftime('%Y')
#         month = date.strftime('%m')
#         day = date.strftime('%d')
#         # _class = Class.objects.get(id=post['classIns'])
#         Attendance.objects.filter(attendance_date__year = year, attendance_date__month = month, attendance_date__day = day).delete()
#         for staff in post.getlist('staff[]'):
#             type = post['type['+staff+']']
#             studInstance = Staffs.objects.get(id = staff)
#             att = Attendance(staff=studInstance,type = type, attendance_date=post['attendance_date'])
#             att.save()
#         resp['status'] = 'success'
#         messages.success(request,"Attendance has been saved successfully.")
#     return HttpResponse(json.dumps(resp),content_type="application/json")


# @login_required
# def save_attendance(request):
#     resp = { 'status': 'failed', 'msg' : '' }
#     if request.method == 'POST':
#         post = request.POST
#         if not post['id'] == '':
#             user = Staffs.objects.get(id = post['id'], is_staff=True)
#             form = forms.Updatestaffs(request.POST, instance=user)
#         else:
#             form = forms.SaveAttendance(request.POST) 

#         if form.is_valid():
#             form.save()
#             if post['id'] == '':
#                 messages.success(request, "Staff has been saved successfully.")
#             else:
#                 messages.success(request, "Staff has been updated successfully.")
#             resp['status'] = 'success'
#         else:
#             for field in form:
#                 for error in field.errors:
#                     if not resp['msg'] == '':
#                         resp['msg'] += str('<br/>')
#                     resp['msg'] += str(f'[{field.name}] {error}')
#     else:
#          resp['msg'] = "There's no data sent on the request"

#     return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def save_attendance(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        post = request.POST

        # Handling Attendance Data
        if 'attendance_date' in post:
            date = datetime.strptime(post['attendance_date'], '%Y-%m-%d')
            year = date.strftime('%Y')
            month = date.strftime('%m')
            day = date.strftime('%d')

            Attendance.objects.filter(attendance_date__year=year, attendance_date__month=month, attendance_date__day=day).delete()
            for staff_id in post.getlist('staff[]'):
                type = post.get(f'type[{staff_id}]', '')
                staff_instance = Staffs.objects.get(id=staff_id)
                att = Attendance(staff=staff_instance, type=type, attendance_date=post['attendance_date'])
                att.save()

            # Updating Response Status
            resp['status'] = 'success'
            messages.success(request, "Attendance has been saved successfully.")

        else:
            resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def manage_attendance_franchise(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_staff'
    context['page_title'] = 'Manage staff'
    if pk is None:
        context['user'] = {}
    else:
        context['user'] = Staffs.objects.get(id=pk)
    
    return render(request, 'Franchise_templates/t_class_date.html', context)

@login_required
def delete_attendance_franchise(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Staff ID is invalid'
    else:
        try:
            Attendance.objects.filter(pk = pk).delete()
            messages.success(request, "Staff has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Staff Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")



@login_required
def laundries_franchise(request):
    context = context_data(request)
    context['page'] = 'laundry'
    context['page_title'] = "laundry List"
    # context['laundries'] = models.Laundry.objects.order_by('-date_added').all()
    user = User.objects.get(id=request.user.id)
    context['laundries'] =  models.Laundry.objects.filter(franchise_details=user).order_by('-date_added').all()
    return render(request, 'Franchise_templates/laundries.html', context)

@login_required
def save_laundry_franchise(request):
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
def view_laundry_franchise(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_laundry'
    context['page_title'] = 'View Laundry'
    if pk is None:
        context['laundry'] = {}
        context['items'] = {}
        # context['pitems'] = {}
    else:
        context['laundry'] = models.Laundry.objects.get(id=pk)
        context['items'] = models.LaundryItems.objects.filter(laundry__id = pk).all()
        # context['pitems'] = models.LaundryProducts.objects.filter(laundry__id = pk).all()
    
    return render(request, 'Franchise_templates/view_laundry.html', context)
    
@login_required
def view_laundry_franchise_walkin(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_laundry'
    context['page_title'] = 'View Laundry'
    if pk is None:
        context['laundry'] = {}
        context['items'] = {}
        # context['pitems'] = {}
    else:
        context['laundry'] = models.Laundry.objects.get(id=pk)
        context['items'] = models.LaundryItems.objects.filter(laundry__id = pk).all()
        # context['pitems'] = models.LaundryProducts.objects.filter(laundry__id = pk).all()
    
    return render(request, 'Franchise_templates/view_laundry_walkin.html', context)
@login_required
def manage_laundry_franchise(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_laundry'
    context['page_title'] = 'Manage laundry'
    context['users'] = models.Customer.objects.all()
    context['fusers'] = models.User.objects.filter(is_franchise = True).all()
    context['coupons'] = models.Coupon.objects.filter(status=1).all()
    # context['products'] = models.Products.objects.filter(delete_flag = 0, status = 1).all()
    context['prices'] = models.Prices.objects.filter(delete_flag = 0, status = 1).all()
    if pk is None:
        context['laundry'] = {}
        context['items'] = {}
        # context['pitems'] = {}
    else:
        context['laundry'] = models.Laundry.objects.get(id=pk)
        context['items'] = models.LaundryItems.objects.filter(laundry__id = pk).all()
        # context['pitems'] = models.LaundryProducts.objects.filter(laundry__id = pk).all()
    
    return render(request, 'Franchise_templates/manage_laundry.html', context)

@login_required
def manage_laundry_franchise_pickup(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_laundry'
    context['page_title'] = 'Manage laundry'
    context['users'] = models.Customer.objects.all()
    context['fusers'] = models.User.objects.filter(is_franchise = True).all()
    context['coupons'] = models.Coupon.objects.filter(status=1).all()
    # context['products'] = models.Products.objects.filter(delete_flag = 0, status = 1).all()
    context['prices'] = models.Prices.objects.filter(delete_flag = 0, status = 1).all()
    if pk is None:
        context['laundry'] = {}
        context['items'] = {}
        # context['pitems'] = {}
    else:
        context['laundry'] = models.Laundry.objects.get(id=pk)
        context['items'] = models.LaundryItems.objects.filter(laundry__id = pk).all()
    return render(request, 'Franchise_templates/manage_laundry_pickup.html', context)

@login_required
def save_laundry_franchise_pickup(request):
    resp = { 'status': 'failed', 'msg' : '', 'id': '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            laundry = models.Laundry.objects.get(id = post['id'])
            form = forms.SaveLaundryPickup(request.POST, instance=laundry)
        else:
            form = forms.SaveLaundryPickup(request.POST) 
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
def update_transaction_form(request, pk = None):
    context = context_data(request)
    context['page'] = 'update_laundry'
    context['page_title'] = 'Update Transaction'
    if pk is None:
        context['laundry'] = {}
    else:
        context['laundry'] = models.Laundry.objects.get(id=pk)
    
    return render(request, 'Franchise_templates/update_status.html', context)

@login_required
def update_transaction_status(request):
    resp = { 'status' : 'failed', 'msg':''}
    if request.POST['id'] is None:
        resp['msg'] = 'Transaction ID is invalid'
    else:
        try:
            models.Laundry.objects.filter(pk = request.POST['id']).update(status = request.POST['status'])
            messages.success(request, "Transaction Status has been updated successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Transaction Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_laundry_franchise(request, pk = None):
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
def reciepts_franchise(request):
    context = context_data(request)
    context['page'] = 'reciepts'
    context['page_title'] = "reciepts List"
    # context['laundries'] = models.Laundry.objects.order_by('-date_added').all()
    user = User.objects.get(id=request.user.id)
    context['laundries'] =  models.Laundry.objects.filter(Q(franchise_details=user) & Q(status=2)).order_by('-date_added').all()
    return render(request, 'Franchise_templates/reciepts.html', context)
@login_required
def view_reciepts_franchise(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_reciepts'
    context['page_title'] = 'View Reciepts'
    if pk is None:
        context['laundry'] = {}
        context['items'] = {}
        # context['pitems'] = {}
    else:
        context['laundry'] = models.Laundry.objects.get(id=pk)
        context['items'] = models.LaundryItems.objects.filter(laundry__id = pk).all()
        # context['pitems'] = models.LaundryProducts.objects.filter(laundry__id = pk).all()
    
    return render(request, 'Franchise_templates/view_reciepts.html', context)

#vendor management
# @login_required
# def laundries_franchise_vendor(request):
#     context = context_data(request)
#     context['page'] = 'laundry'
#     context['page_title'] = "laundry List"
#     # context['laundries'] = models.Laundry.objects.order_by('-date_added').all()
#     user = User.objects.get(id=request.user.id)
#     context['laundries'] =  models.Laundry.objects.filter(franchise_details=user).order_by('-date_added').all()
#     return render(request, 'Franchise_templates/laundries.html', context)
@login_required
def laundries_franchise_vendor(request):
    context = context_data(request)
    context['page'] = 'laundry'
    context['page_title'] = "Laundry List"

    user = User.objects.get(id=request.user.id)
    context['laundries'] = models.Laundry.objects.filter(Q(vendor_details__isnull=False) & Q(franchise_details=user)).order_by('-date_added').all()
    # context['laundries'] = models.Laundry.objects.filter(franchise_details=user).order_by('-date_added').all()
    return render(request, 'Franchise_templates/laundries_vendor.html', context)

@login_required
def save_laundry_franchise_vendor(request):
    resp = { 'status': 'failed', 'msg' : '', 'id': '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            laundry = models.Laundry.objects.get(id = post['id'])
            form = forms.SaveLaundryVendor(request.POST, instance=laundry)
        else:
            form = forms.SaveLaundryVendor(request.POST) 
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
def view_laundry_franchise_vendor(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_laundry'
    context['page_title'] = 'View Laundry'
    if pk is None:
        context['laundry'] = {}
        context['items'] = {}
        # context['pitems'] = {}
    else:
        context['laundry'] = models.Laundry.objects.get(id=pk)
        context['items'] = models.LaundryItems.objects.filter(laundry__id = pk).all()
        # context['pitems'] = models.LaundryProducts.objects.filter(laundry__id = pk).all()
    
    return render(request, 'Franchise_templates/view_laundry_vendor.html', context)

@login_required
def manage_laundry_franchise_vendor(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_laundry'
    context['page_title'] = 'Manage laundry'
    context['users'] = models.Customer.objects.all()
    context['fusers'] = models.User.objects.filter(is_franchise = True).all()
    context['vusers'] = models.User.objects.filter(is_vendor = True).all()
    context['coupons'] = models.Coupon.objects.filter(status=1).all()
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
    
    return render(request, 'Franchise_templates/manage_laundry_vendor.html', context)


@login_required
def update_transaction_form(request, pk = None):
    context = context_data(request)
    context['page'] = 'update_laundry'
    context['page_title'] = 'Update Transaction'
    if pk is None:
        context['laundry'] = {}
    else:
        context['laundry'] = models.Laundry.objects.get(id=pk)
    
    return render(request, 'Franchise_templates/update_status.html', context)

@login_required
def update_transaction_status(request):
    resp = { 'status' : 'failed', 'msg':''}
    if request.POST['id'] is None:
        resp['msg'] = 'Transaction ID is invalid'
    else:
        try:
            models.Laundry.objects.filter(pk = request.POST['id']).update(status = request.POST['status'])
            messages.success(request, "Transaction Status has been updated successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Transaction Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_laundry_franchise_vendor(request, pk = None):
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
def reciepts_franchise_vendor(request):
    context = context_data(request)
    context['page'] = 'reciepts'
    context['page_title'] = "reciepts List"
    # context['laundries'] = models.Laundry.objects.order_by('-date_added').all()
    user = User.objects.get(id=request.user.id)
    context['laundries'] =  models.Laundry.objects.filter(Q(franchise_details=user) & Q(status=2)).order_by('-date_added').all()
    return render(request, 'Franchise_templates/reciepts.html', context)
@login_required
def view_reciepts_franchise_vendor(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_reciepts'
    context['page_title'] = 'View Reciepts'
    if pk is None:
        context['laundry'] = {}
        context['items'] = {}
        # context['pitems'] = {}
    else:
        context['laundry'] = models.Laundry.objects.get(id=pk)
        context['items'] = models.LaundryItems.objects.filter(laundry__id = pk).all()
        # context['pitems'] = models.LaundryProducts.objects.filter(laundry__id = pk).all()
    
    return render(request, 'Franchise_templates/view_reciepts.html', context)
# Assuming you have already imported required libraries and models at the beginning of your file

# def barcode_scan_view(request, pk=None):
#     context = context_data(request)
#     if pk is None:
#         context['laundry'] = {}
#     else:
#         context['laundry'] = Laundry.objects.get(id=pk)
#     print(context['laundry'])
#     return render(request, 'Franchise_templates/scan.html')

# def process_barcode_view(request):
#     context = context_data(request)
#     # if request.method == 'POST':
#     if request.POST['id'] is None:
#         data = request.POST.copy()
#         # data['id'] = pk
#         data_uri = request.POST.get('data_uri', '')
#         barcode_data = decode_barcode(data_uri)
#         if barcode_data:
#             # Save the barcode data to the database
#             print(barcode_data)
#             # print(pk)
#             # laundry_instance = models.Laundry.objects.get(pk=pk)
#             # print(laundry_instance)
#             # laundry_instance.barcode = barcode_data
#             # laundry_instance.save()
#             models.Laundry.objects.filter(pk = request.POST['id']).update(barcode = request.POST['barcode_data'])
            
#             return HttpResponse(json.dumps({'success': True, 'message': 'Barcode Scanned Successfully'}), content_type='application/json')
#         else:
#             return HttpResponse(json.dumps({'success': False, 'message': 'Invalid barcode data'}), content_type='application/json')
#     else:
#         return HttpResponse(json.dumps({'success': False, 'message': 'Invalid request method'}), content_type='application/json')
# from django.shortcuts import render
# from .models import Laundry

# def barcode_scan_view(request, pk=None):
#     context = {}
#     if pk is None:
#         context['laundry'] = {}
#     else:
#         context['laundry'] = Laundry.objects.get(pk=pk)
        
#     # Process barcode data and update Laundry model
#     return render(request, 'Franchise_templates/scan.html', context)


# from django.shortcuts import render
# from django.http import HttpResponse
# import json

# # from .models import Laundry
# # from .utils import decode_barcode

# # def process_barcode_view(request):
# #     post = request.POST
# #     if request.method == 'POST':
# #         data_uri = request.POST.get('data_uri', '')
        
# #         # Ensure 'id' key exists in the POST data and set pk accordingly
# #         # pk = request.POST.get('id', pk)

# #         barcode_data = decode_barcode(data_uri)
# #         # print(pk)
# #         if not post['id'] == '':
# #             # Save the barcode data to the database
# #             print(barcode_data)
# #             laundry = models.Laundry.objects.get(id=post['id'])
# #             # form = forms.SaveLaundry(request.POST, instance=laundry)
# #             laundry.barcode = barcode
# #             # laundry_instance = Laundry.objects.get(pk=pk)
# #             # laundry_instance.barcode = barcode_data
# #             laundry.save()
# #             # models.Laundry.objects.filter(pk = request.POST['id']).update(barcode = request.POST['barcode_data'])
# #             return HttpResponse(json.dumps({'success': True, 'message': 'Barcode Scanned Successfully'}), content_type='application/json')
# #         else:
# #             return HttpResponse(json.dumps({'success': False, 'message': 'Invalid barcode data'}), content_type='application/json')
# #     else:
# #         return HttpResponse(json.dumps({'success': False, 'message': 'Invalid request method'}), content_type='application/json')

# from django.http import HttpResponse
# from django.contrib import messages
# import json

# def process_barcode_view(request):
#     resp = {'status': 'failed', 'msg': ''}
    
#     user_id = request.POST.get('id')
#     if user_id is None:
#         resp['msg'] = 'User ID is invalid'
#     else:
#         data_uri = request.POST.get('data_uri', '')

#         barcode_data = decode_barcode(data_uri)
#         try:
#             # Using .get() instead of .filter() to retrieve a single object
#             laundry = Laundry.objects.get(pk=user_id)
#             laundry.barcode = barcode_data
#             laundry.save()
#             messages.success(request, "User Status has been updated successfully.")
#             resp['status'] = 'success'
#         except Laundry.DoesNotExist:
#             resp['msg'] = "Laundry object with the given ID does not exist"
#         except Exception as e:
#             resp['msg'] = f"Updation Failed: {str(e)}"

#     return HttpResponse(json.dumps(resp), content_type="application/json")

def barcode_scan_view(request, pk=None):
    context = context_data(request)
    if pk is None:
        context['laundry'] = {}
    else:
        context['laundry'] = Laundry.objects.get(id=pk)
    print(pk)
    return render(request, 'Franchise_templates/scan.html', context)


from django.http import HttpResponse
import json
from . import models  # Import your models module

def process_barcode_view(request):
    if request.method == 'POST':
        data_uri = request.POST.get('data_uri', '')
        barcode_data = decode_barcode(data_uri)
        post = request.POST
        resp = {'success': False, 'message': ''}  # Define the resp dictionary
        
        user_id = post.get('id')
        if user_id is None:
            resp['message'] = 'User ID is invalid'
        else:
            if barcode_data:
                try:
                    laundry = models.Laundry.objects.get(id=user_id)
                    laundry.barcode = barcode_data
                    laundry.save()
                    resp['success'] = True
                    resp['message'] = 'Barcode Scanned Successfully'
                except models.Laundry.DoesNotExist:
                    resp['message'] = 'Laundry object with the given ID does not exist'
                except Exception as e:
                    resp['message'] = f'Error: {str(e)}'
            else:
                resp['message'] = 'Invalid barcode data'

        return HttpResponse(json.dumps(resp), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False, 'message': 'Invalid request method'}), content_type='application/json')


# Function to decode barcode from image data URI
def decode_barcode(data_uri):
    _, encoded_image = data_uri.split(',', 1)
    image = base64.b64decode(encoded_image)
    image = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    decoded_objects = decode(image)
    if decoded_objects:
        barcode_data = decoded_objects[0].data.decode('utf-8')
        if 100000 <= int(barcode_data) <= 199999:
            return barcode_data
    return None
# tickets
@login_required
def tickets_franchise(request):
  
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
               return redirect('allcomplaints_franchise')
    else:
        
        tickets_form=TicketsForm(request.POST)
    context={'tickets_form':tickets_form,}
    context['fusers'] = models.User.objects.filter(is_franchise = True).all()
    return render(request,'Franchise_templates/add_tickets.html',context)



@login_required
def list_franchise(request):
    c=Tickets.objects.filter(user=request.user).exclude(status='1')
    result=Tickets.objects.filter(user=request.user).exclude(Q(status='3') | Q(status='2'))
    # c=Tickets.objects.all()
    args={'c':c,'result':result}
    return render(request,'Franchise_templates/Complaints.html',args)

@login_required
def plist_franchise(request):
    result=Tickets.objects.filter(user=request.user).exclude(Q(status='1') | Q(status='3'))
    c=Tickets.objects.all()
    args={'result':result}
    return render(request,'Franchise_templates/progresscomplaint.html',args)

@login_required
def allcomplaints_franchise(request):
      
        user = User.objects.get(id=request.user.id)
        c=Tickets.objects.filter(Franchise_branch=user).exclude(status='1')
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
                        return HttpResponseRedirect(reverse('allcomplaints_franchise'))
                else:
                        return render(request,'Franchise_templates/AllComplaints.html')
                 #testing

        else:
                forms=statusupdate()
        # c=Complaint.objects.all().exclude(status='1')
           
        args={'c':c,'forms':forms,'comp':comp}
        return render(request,'Franchise_templates/AllComplaints.html',args)
    
@login_required
def solved_franchise(request):
        
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
                        return render(request,'Franchise_templatess/solved.html')
                 #testing

        else:
                forms=statusupdate()
        c=Tickets.objects.all().exclude(Q(status='3') | Q(status='2'))
        
        args={'c':c,'forms':forms,'comp':comp}
        return render(request,'Franchise_templates/solved.html',args)  

@login_required
def daily_report_franchise(request, date = None):
    context = context_data(request)
    context['page'] = 'view_laundry'
    context['page_title'] = 'Daily Transaction Report'
    
    if date is None :
        # date = datetime.strptime(date, '%Y-%m-%d')
        # year = date.strftime('%Y')
        # month = date.strftime('%m')
        # day = date.strftime('%d')
        date = datetime.now()
        year = date.strftime('%Y')
        month = date.strftime('%m')
        day = date.strftime('%d')
    else:
        # date = datetime.strptime(date, '%Y-%m-%d')
        # year = date.strftime('%Y')
        # month = date.strftime('%m')
        # day = date.strftime('%d')
        date =datetime.strptime(date, '%Y-%m-%d')
        year = date.strftime('%Y')
        month = date.strftime('%m')
        day = date.strftime('%d')

    context['date'] = date
    user = User.objects.get(id = request.user.id)
    context['laundries'] = models.Laundry.objects.filter(
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
            franchise_details= user,
            status=2
        )
    grand_total = 0
    for laundry in context['laundries']:
        grand_total += float(laundry.total_amount)
    context['grand_total'] = grand_total
    
    return render(request, 'Franchise_templates/report.html', context)

# @login_required
# def daily_report(request, date= None):
#     context = context_data(request)
#     context['page'] = 'view_laundry'
#     context['page_title'] = 'Daily Transaction Report'
#     if date is None :
#         # date = datetime.strptime(date, '%Y-%m-%d')
#         # year = date.strftime('%Y')
#         # month = date.strftime('%m')
#         # day = date.strftime('%d')
#         date = datetime.now()
#         year = date.strftime('%Y')
#         month = date.strftime('%m')
#         day = date.strftime('%d')
#     else:
#         # date = datetime.strptime(date, '%Y-%m-%d')
#         # year = date.strftime('%Y')
#         # month = date.strftime('%m')
#         # day = date.strftime('%d')
#         date =datetime.strptime(date, '%Y-%m-%d')
#         year = date.strftime('%Y')
#         month = date.strftime('%m')
#         day = date.strftime('%d')

#     if request.method =='POST':
#         date_from = request.POST.get('date_from')
#         date_to = request.POST.get('date_to')
        

        
#         context['laundries'] = models.Laundry.objects.filter(pickup_date__lte=date_to, pickup_date__gte=date_from)
#     # context['date'] = date
#     # context['laundries'] = models.Laundry.objects.filter(
#     #         date_added__year = year,
#     #         date_added__month = month,
#     #         date_added__day = day,
#     #     )
#         grand_total = 0
#         for laundry in context['laundries']:
#             grand_total += float(laundry.total_amount)
#         context['grand_total'] = grand_total
    
#     return render(request, 'Franchise_templates/report.html', context)

@login_required
def report_view_franchise(request):
    sales_df =None
    merged_df =None
    positions_df = None
    df =None
    chart = None
    no_data = None
    search_form = SalesSearchForm(request.POST or None)
    # report_form = ReportForm()
    if request.method =='POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')

        user = User.objects.get(id = request.user.id)
        sale_qs = Laundry.objects.filter(pickup_date__lte=date_to, pickup_date__gte=date_from, franchise_details= user)
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
    return render(request, 'Franchise_templates/report_generation.html',context)
# Chats
@login_required
def chat_franchise(request):
    User = get_user_model()
    users = User.objects.filter(is_superuser=True)
    print(users)
    chats = {}
    if request.method == 'GET' and 'u' in request.GET:
        # chats = chatMessages.objects.filter(Q(user_from=request.user.id & user_to=request.GET['u']) | Q(user_from=request.GET['u'] & user_to=request.user.id))
        chats = chatMessages.objects.filter(Q(user_from=request.user.id, user_to=request.GET['u']) | Q(user_from=request.GET['u'], user_to=request.user.id))
        chats = chats.order_by('date_created')
    context = {
        "page":"home",
        "users":users,
        "chats":chats,
        "chat_id": int(request.GET['u'] if request.method == 'GET' and 'u' in request.GET else 0)
    }
    print(request.GET['u'] if request.method == 'GET' and 'u' in request.GET else 0)
    return render(request,"Franchise_templates/chat.html",context)




def get_messages_franchise(request):
    chats = chatMessages.objects.filter(Q(id__gt=request.POST['last_id']),Q(user_from=request.user.id, user_to=request.POST['chat_id']) | Q(user_from=request.POST['chat_id'], user_to=request.user.id))
    new_msgs = []
    for chat in list(chats):
        data = {}
        data['id'] = chat.id
        data['user_from'] = chat.user_from.id
        data['user_to'] = chat.user_to.id
        data['message'] = chat.message
        data['date_created'] = chat.date_created.strftime("%Y-%m-%d %H:%M")
        print(data)
        new_msgs.append(data)
    return HttpResponse(json.dumps(new_msgs), content_type="application/json")

def send_chat_franchise(request):
    resp = {}
    User = get_user_model()
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
#API Views
def default_category(request):
    if request.method == 'GET':
        categories = Prices.objects.filter(category='t shirt')
        print(categories)
        # laundry_types = list(categories.values_list('laundry_type', flat=True).distinct())
        laundry_types = []
        sub_category = []
        for i in categories:
            if i.laundry_type not in laundry_types:

                laundry_types.append(i.laundry_type)
        return JsonResponse({'categories':'t-shirt', 'laundry_types':laundry_types})

def get_laundrytypes(request):
    if request.method=='POST':
        data = json.loads(request.body)
        category = data['çategory']
        categories = list(Prices.objects.filter(category=category))
        laundry_types = list(categories.values_list('laundry_type', flat=True).distinct())
        return JsonResponse({'laundry_types':laundry_types})

# franchise----live link ===CCTV  --->start
def CCTV_form(request):
    if request.method == 'POST':
        name = request.POST['name']
        live_stream_url = request.POST['live_stream_url']
        CCTV.objects.create(Franchise_name=name, Live_stream_url=live_stream_url)
        messages.success(request, 'CCTV live link sent successfully to admin.')
        return redirect('CCTV_form')

    return render(request, 'Franchise_templates/CCTV_form.html')



# franchise----live link ===CCTV  --->end

# @login_required
# def manage_product_franchise(request, pk = None):
#     context = context_data(request)
#     context['page'] = 'manage_product'
#     context['page_title'] = 'Manage product'
#     if pk is None:
#         context['product'] = {}
                
#     else:
#         context['product'] = models.ProductsFranchise.objects.get(id=pk)
    
#     return render(request, 'Franchise_templates/manage_product.html', context)
@login_required
def products_all(request):
    context = context_data(request)
    context['page'] = 'Product'
    context['page_title'] = "Product List"
    context['products'] = models.Products.objects.filter(delete_flag = 0).all()
    return render(request, 'Franchise_templates/products.html', context)


@login_required
def view_product_all(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_product'
    context['page_title'] = 'View Product'
    if pk is None:
        context['product'] = {}
        #context['stockinsfranchise'] = {}
    else:
        context['product'] = models.Products.objects.get(id=pk)
        # context['stockinsfranchise'] = models.StockInFranchise.objects.filter(product__id=pk)
        # context['stockouts'] = models.LaundryProducts.objects.filter(product__id=pk).order_by('productpurchase__code')
    
    return render(request, 'Franchise_templates/view_product.html', context)


@login_required
def products_franchise(request):
    context = context_data(request)
    context['page'] = 'Product'
    context['page_title'] = "Product List"
    user = User.objects.get(id=request.user.id)
    context['franchiseproducts'] = models.FranchiseProducts.objects.filter(delete_flag = 0, franchise_details=user).all()
    return render(request, 'Franchise_templates/products_instock.html', context)

@login_required
def manage_product_franchise(request,pid = None, pk = None):
    context = context_data(request)
    context['page'] = 'manage_stockin'
    context['page_title'] = 'Manage Stockin'
    context['pid'] = pid
    print(pid)
    print(pk)
    context['fusers'] = models.Products.objects.filter(status = 1).all()
    if pk is None:
        context['franchiseproduct'] = {}
                
    else:
        context['franchiseproduct'] = models.FranchiseProducts.objects.get(id=pk)

    
    return render(request, 'Franchise_templates/manage_product.html', context)
#corrected

     

# @login_required
# def save_product_franchise(request):
#     resp = { 'status': 'failed', 'msg' : '', 'id': '' }
#     if request.method == 'POST':
#         post = request.POST
#         if not post['id'] == '':
#             franchiseproduct = models.FranchiseProducts.objects.get(id = post['id'])
#             form = forms.SaveProductsFranchise(request.POST,request.FILES, instance=franchiseproduct )
#         else:
#             form = forms.SaveProductsFranchise(request.POST) 

#         if form.is_valid():
#             form.instance.franchise_details = request.user
#             form.save()
#             if post['id'] == '':
#                 messages.success(request, "Product has been saved successfully.")
#                 pid = models.FranchiseProducts.objects.last().id
#                 resp['id'] = pid
#             else:
#                 messages.success(request, "Product has been updated successfully.")
#                 resp['id'] = post['id']
#             resp['status'] = 'success'
#         else:
#             for field in form:
#                 for error in field.errors:
#                     if not resp['msg'] == '':
#                         resp['msg'] += str('<br/>')
#                     resp['msg'] += str(f'[{field.name}] {error}')
#     else:
#          resp['msg'] = "There's no data sent on the request"

#     return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def save_product_franchise(request):
    resp = { 'status': 'failed', 'msg' : '', 'id': '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            franchiseproduct = models.FranchiseProducts.objects.get(id = post['id'])
            form = forms.SaveProductsFranchise(request.POST,request.FILES, instance=franchiseproduct )
        else:
            form = forms.SaveProductsFranchise(request.POST) 

        if form.is_valid():
            form.instance.franchise_details = request.user
            form.save()
            if post['id'] == '':
                messages.success(request, "Product has been saved successfully.")
                pid = models.FranchiseProducts.objects.last().id
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
def view_productsfranchise(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_product'
    context['page_title'] = 'View Product'
    print(pk)
    if pk is None:
        context['franchiseproduct'] = {}
        context['franchisestockins'] = {}
        context['franchisestockouts'] = {}
    else:
        context['franchiseproduct'] = models.FranchiseProducts.objects.get(id=pk)
        context['franchisestockins'] = models.FranchiseStockIn.objects.filter(franchiseproduct__id=pk)
        context['franchisestockouts'] = models.FranchiseStockOut.objects.filter(franchiseproduct__id=pk)
        # context['stockouts'] = models.LaundryProducts.objects.filter(product__id=pk).order_by('productpurchase__code')
    
    return render(request, 'Franchise_templates/view_product_franchise.html', context)

@login_required
def delete_product_franchise(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Product ID is invalid'
    else:
        try:
            models.FranchiseProducts.objects.filter(pk = pk).update(delete_flag = 1)
            messages.success(request, "Product has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Product Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def manage_stockin_franchise(request, pid = None, pk = None):
    context = context_data(request)
    context['page'] = 'manage_stockin'
    context['page_title'] = 'Manage Stockin'
    context['pid'] = pid
    print(pid)
    print(pk)
    context['fusers'] = models.User.objects.filter(is_franchise = True).all()
    if pk is None:
        context['franchisestockin'] = {}
    else:
        context['franchisestockin'] = models.FranchiseStockIn.objects.get(id=pk)
    
    return render(request, 'Franchise_templates/manage_stockin.html', context)
    
    
@login_required
def save_stockin_franchise(request):
    resp = { 'status': 'failed', 'msg' : ''}
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            franchisestockin = models.FranchiseStockIn.objects.get(id = post['id'])
            form = forms.SaveStockInFranchise(request.POST, instance=franchisestockin)
        else:
            form = forms.SaveStockInFranchise(request.POST) 
        
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
def delete_stockin_franchise(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Stock-in ID is invalid'
    else:
        try:
            models.FranchiseStockIn.objects.filter(pk = pk).delete()
            messages.success(request, "Stock Entry Details has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Stock Entry Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def manage_stockout_franchise(request, pid = None, pk = None):
    context = context_data(request)
    context['page'] = 'manage_stockout'
    context['page_title'] = 'Manage Stockout'
    context['pid'] = pid
    print(pid)
    print(pk)
    context['fusers'] = models.User.objects.filter(is_franchise = True).all()
    if pk is None:
        context['franchisestockout'] = {}
    else:
        context['franchisestockout'] = models.FranchiseStockOut.objects.get(id=pk)
    
    return render(request, 'Franchise_templates/manage_stockout.html', context)
    
    
@login_required
def save_stockout_franchise(request):
    resp = { 'status': 'failed', 'msg' : ''}
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            franchisestockout = models.FranchiseStockOut.objects.get(id = post['id'])
            form = forms.SaveStockOutFranchise(request.POST, instance=franchisestockout)
        else:
            form = forms.SaveStockOutFranchise(request.POST) 
        
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
def delete_stockout_franchise(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Stock-in ID is invalid'
    else:
        try:
            models.FranchiseStockIn.objects.filter(pk = pk).delete()
            messages.success(request, "Stock Entry Details has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Stock Entry Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

    
@login_required
def manage_usedproduct(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_product_used'
    context['page_title'] = 'Manage product_used'
    context['products'] = models.FranchiseProducts.objects.filter(delete_flag = 0, status = 1).all()
    # context['prices'] = models.Prices.objects.filter(delete_flag = 0, status = 1).all()
    if pk is None:
        # context['productpurchase'] = {}
        # context['items'] = {}
        context['pitems'] = {}
    else:
        # context['productpurchase'] = models.Productpurchase.objects.get(id=pk)
        # context['items'] = models.LaundryItems.objects.filter(laundry__id = pk).all()
        context['pitems'] = models.LaundryProducts.objects.filter(productpurchase__id = pk).all()
    
    return render(request, 'Franchise_templates/manage_product_used.html', context)
    
@login_required
def save_usedproduct(request):
    resp = { 'status': 'failed', 'msg' : '', 'id': '' }
    if request.method == 'POST':
        post = request.POST
        # if not post['id'] == '':
        #     productpurchase = models.Productpurchase.objects.get(id = post['id'])
        #     form = forms.SaveProductpurchase(request.POST, instance=productpurchase)
        # else:
        #     form = forms.SaveProductpurchase(request.POST) 
        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Laundry has been saved successfully.")
                pid = models.Productpurchase.objects.last().id
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
    
    return render(request, 'Franchise_templates/view_productpurchase.html', context)
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

#coupon
@login_required
def coupon_franchise(request):
    context = context_data(request)
    context['page'] = 'Coupon'
    context['page_title'] = "Coupon List"
    user = User.objects.get(id=request.user.id)
    context['coupons'] =  models.Coupon.objects.filter(Q(franchise_details=user) | Q(franchise_details=None))
    return render(request, 'Franchise_templates/coupon_code.html', context)
@login_required
def manage_coupon_franchise(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_coupon'
    context['page_title'] = 'Manage coupon'
    if pk is None:
        context['coupon'] = {}
    else:
        context['coupon'] = Coupon.objects.get(id=pk)
    context['fusers'] = models.User.objects.filter(is_franchise = True).all()
    return render(request, 'Franchise_templates/manage_coupon.html', context)

@login_required
def save_coupon_franchise(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            coupon = Coupon.objects.get(id = post['id'])
            form = forms.SaveCouponFranchise(request.POST, instance=coupon)
        else:
            form = forms.SaveCouponFranchise(request.POST) 

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
def delete_coupon_franchise(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'coupon ID is invalid'
    else:
        try:
            Coupon.objects.filter(pk = pk).delete()
            messages.success(request, "coupon has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting coupon Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")
@login_required
def view_coupon_franchise(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_coupon'
    context['page_title'] = 'View coupon'
    if pk is None:
        context['coupon'] = {}
        
    else:
        context['coupon'] = Coupon.objects.get(id=pk)
        
    
    return render(request, 'Franchise_templates/view_coupon.html', context)


    # Notifications


@login_required
def render_restock_request_modal(request, pk=None):
    context = context_data(request)
    if pk is None:
        context['franchiseproducts'] = {}
    else:
        context['franchiseproducts'] = models.FranchiseProducts.objects.get(id=pk)
    print(pk)
    
    print(context)
    return render(request, 'Franchise_templates/restock_popup.html', context)

@login_required
def send_restock_request(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        product_id = request.POST.get('id')
        quantity = request.POST.get('quantity')
        print(product_id)
        print(quantity)
        # Get the product name from your model
        try:
            product = FranchiseProducts.objects.get(pk=product_id)
            product_name = product.name
            print(product_name)
        except FranchiseProducts.DoesNotExist:
            return JsonResponse({'status': 'error'})

        # Create a notification for the admin
        sender = request.user  # The franchise sending the request
        heading = f" Urgent Restocking Request for {product_name}"
        message =  (
            f"We have an urgent restocking request for the following product:\n\n"
            f"Product: {product_name}\n"
            f"Quantity Needed: {quantity}\n\n\n"
            f"Please take immediate action to ensure the availability of this product as our inventory is running low. Your prompt attention to this matter is greatly appreciated.\n\n"
            f"Thank you, {sender.username}\n"
            f"Contact: [Your Contact Information]"
        )

        notification = Notification.objects.create(sender=sender, message=message, heading=heading, quantity=quantity)
        messages.success(request, "Restock Request Sent successfully.")
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})



@login_required
def send_cancel_request(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        pk = request.POST.get('pk')
        # Get the laundry object based on the pk
        try:
            laundry = Laundry.objects.get(pk=pk)  # Replace with your model name
        except Laundry.DoesNotExist:
            return JsonResponse({'status': 'error'})

        # Create a notification for the admin
        sender = request.user
        heading = f" Cancel Order Request"
        # code_link = f"<a href='{reverse('view-laundry-pk', args=[laundry.pk])}'>{laundry.code}</a>"
        message = f"{sender.username} has requested to cancel the order with code {laundry.code}. Please review and take appropriate action."

        notification = Notification.objects.create(sender=sender, message=message, heading=heading)
        messages.success(request, "Cancel Request Sent successfully.")
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

# notification from admin
@login_required
def franchise_notifications_view(request):
    notifications_franchise = Franchise_Notification.objects.all().order_by('-created_at') # Get unread notifications
    return render(request, 'Franchise_templates/franchise-inbox_notifications_list.html', {'notifications_franchise': notifications_franchise})


from django.shortcuts import get_object_or_404
@login_required
def franchise_inbox_convo(request, notification_id):
    print("Notification ID:", notification_id)
    # Retrieve the specific notification using the notification_id from the URL
    notification = get_object_or_404(Franchise_Notification, id=notification_id)
    
    # Update the notification to mark it as read (assuming you want to do this)
    notification.is_read = True
    notification.save()
    
    # Query other unread notifications from the same sender
    # all_notifications = Notification.objects.filter(Q(sender=request.user) & Q(id=notification_id))
    all_notifications = Franchise_Notification.objects.filter(id=notification_id)
    
    print("User ID:", request.user.id) 

    # return render(request, 'Franchise_templates/app-inbox-conversation.html', {'notifications': unread_notifications})
    return render(request, 'Franchise_templates/franchise-inbox_conversation.html', {'notifications': all_notifications})    


def franchise_mark_notification_read(request):
    if request.method == 'POST' and request.is_ajax():
        notification_id = request.POST.get('notification_id')
        try:
            notification = Franchise_Notification.objects.get(id=notification_id)
            notification.is_read = True
            notification.save()
            return JsonResponse({'status': 'success'})
        except Franchise_Notification.DoesNotExist:
            return JsonResponse({'status': 'error'})



def fetch_contact_franchise(request):
    if request.method == "GET":
        username = request.GET.get("username", "")
        try:
            user = Customer.objects.get(id=username)
            contact = user.phone if user.phone else ""
            return JsonResponse({"contact": contact})
        except User.DoesNotExist:
            return JsonResponse({"contact": ""})
    return JsonResponse({"contact": ""})

def fetch_price_franchise(request):
    if request.method == "GET":
        name = request.GET.get("name", "")
        try:
            user = models.Products.objects.get(name=name)
            price = user.price if user.price else ""
            return JsonResponse({"price": price})
        except User.DoesNotExist:
            return JsonResponse({"price": ""})
    return JsonResponse({"price": ""})


# timeslot
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Timeslot

def timeslot_franchise(request):
    return render(request, 'Franchise_templates/timeslot.html')

from django.core import serializers
from datetime import datetime, timedelta

def get_timeslots_franchise(request):
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




def save_timeslots_franchise(request):
    if request.method == 'POST':
        timeslots_data = json.loads(request.body)
        if timeslots_data:
            try:
                for timeslot_data in timeslots_data:
                    start_time, end_time = timeslot_data['timeslot'].split(' - ')
                    day_of_week = timeslot_data['day_of_week']

                    Timeslot.objects.create(
                        start_time=start_time.strip(),
                        end_time=end_time.strip(),
                        day_of_week=day_of_week,
                        status=timeslot_data['status']
                    )
                
                return JsonResponse({'message': 'Timeslots saved successfully'}, status=200)
            except Exception as e:
                return JsonResponse({'message': 'Error saving timeslots: ' + str(e)}, status=500)
        else:
            return JsonResponse({'message': 'No timeslots data provided'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)