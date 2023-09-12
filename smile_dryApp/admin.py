from django.contrib import admin
from .models import User, Franchise_User, FranchiseStockIn, Coupon, Tickets, Products, Contact, TermsCondition, Laundry, Vendor, Rider, Franchise_Notification,Notification, FranchiseProducts,Staffs, Productpurchase

# Register your models here.
admin.site.register(User)
admin.site.register(Franchise_User)
admin.site.register(Vendor)
admin.site.register(Rider)
admin.site.register(Staffs)
admin.site.register(Coupon)
admin.site.register(Products)
admin.site.register(Contact)
admin.site.register(TermsCondition)
admin.site.register(Laundry)
admin.site.register(Notification)
admin.site.register(Franchise_Notification)
admin.site.register(FranchiseProducts)
admin.site.register(Productpurchase)
admin.site.register(Tickets)
admin.site.register(FranchiseStockIn)
