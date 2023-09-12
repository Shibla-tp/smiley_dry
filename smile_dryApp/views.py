from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, TicketsForm, statusupdate
from smile_dryApp.forms import SignUpForm, LoginForm, TicketsForm, statusupdate
from django.contrib.auth import authenticate, login, logout
import datetime
from django.shortcuts import redirect, render
import json
from django.contrib import messages
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import HttpResponse
from smile_dryApp import models, forms
from smile_dryApp.models import User, Tickets
from django.db.models import Q, Sum
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse
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


def index(request):
    return render(request, 'Super_admin_templates/index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'Super_admin_templates/register.html', {'form': form, 'msg': msg})

def login_page(request):
    context = context_data(request)
    context['topbar'] = False
    context['footer'] = False
    context['page_name'] = 'login'
    context['page_title'] = 'Login'
    return render(request, 'Super_admin_templates/login.html', context)

def login_view(request):
    context = context_data(request)
    context['topbar'] = False
    context['footer'] = False
    context['page_name'] = 'login'
    context['page_title'] = 'Login'
    logout(request)
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username1 = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password')
            user = authenticate(username=username1, password=password1)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_superuser:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_customer:
                login(request, user)
                return redirect('customer')
            elif user is not None and user.is_franchise and user.status == '1':
                login(request, user)
                return redirect('franchise')
            elif user is not None and user.is_vendor and user.status == '1':
                login(request, user)
                return redirect('franchise')
            elif user is not None and user.is_rider and user.status == '1':
                login(request, user)
                return redirect('rider')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'Super_admin_templates/login.html', {'form': form, 'msg': msg})

def logout_user(request):
    logout(request)
    return redirect('login-page')



