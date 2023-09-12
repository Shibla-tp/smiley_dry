from .models import Tickets, Customer, User, Notification,Franchise_Notification
from django.db.models import Q
# from django.contrib.auth.decorators import login_required

def customer_context(request):
    customer_count = Customer.objects.filter(is_customer=True).count()
    context = {
        
        'customer_count': customer_count,
        
    }

    return context

# @login_required
# def franchise_customer_context(request):
#     user = User.objects.get(id=request.user.id)
#     franchise_customer_count = Customer.objects.filter(Q(is_customer=True) & Q(franchise_city=user)).count()
    
#     context = {
        
#         'franchise_customer_count': franchise_customer_count,
        
#     }

#     return context

def complaint_context(request):
    tickets_count = Tickets.objects.all().count()
    context = {
        
        'tickets_count': tickets_count,
        
    }

    return context

# def login_user_context(request):
#     user = User.objects.get(id=request.user.id)
#     context = {
        
#         'user': user,
        
#     }

#     return context

def admin_dashboard_notifications(request):
    # Retrieve the restock notifications
    notification_count = Notification.objects.filter(is_read=False).count()
    restock_notifications = Notification.objects.all().order_by('-created_at')[:5]

    context = {
        'notification_count': notification_count,
        'restock_notifications': restock_notifications,
    }
    
    return context


def franchise_dashboard_notifications(request):
    # Retrieve the restock notifications
    notification_count_franchise =Franchise_Notification.objects.filter(is_read=False).count()
    admin_notifications = Franchise_Notification.objects.all().order_by('-created_at')[:5]

    context = {
        'notification_count_franchise': notification_count_franchise,
        'admin_notifications': admin_notifications,
    }
    
    return context