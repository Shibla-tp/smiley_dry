from django.urls import path, include
from . import views, Super_views, Franchise_views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin





urlpatterns = [
    #login system
    path('', views.login_view, name= 'login-view'),
    path('login',views.login_page,name='login-page'),
    path('login_view', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('adminpage/', Super_views.admin, name='adminpage'),
    path('customer/', Super_views.customer, name='customer'),
    path('vendor/', Super_views.vendor, name='vendor'),
    path('rider/', Super_views.rider, name='rider'),
    #Super admin profile
    path('profile',Super_views.profile,name='profile-page'),
    path('update_password',Super_views.update_password,name='update-password'),
    path('update_profile',Super_views.update_profile,name='update-profile'),
    #logout
    path('logout',Super_views.logout_user,name='logout'),
    #T&C
    path('terms_conditions',Super_views.terms_conditions,name='terms_conditions-page'),
    path('manage_terms_conditions',Super_views.manage_terms_conditions,name='manage-terms_conditions'),
    path('manage_terms_conditions/<int:pk>',Super_views.manage_terms_conditions,name='manage-terms_conditions-pk'),
    path('save_terms_conditions',Super_views.save_terms_conditions,name='save-terms_conditions'),
    #About Us
    path('about_us',Super_views.about_us,name='about_us-page'),
    path('manage_about_us',Super_views.manage_about_us,name='manage-about_us'),
    path('manage_about_us/<int:pk>',Super_views.manage_about_us,name='manage-about_us-pk'),
    path('save_about_us',Super_views.save_about_us,name='save-about_us'),
    #user management
    path('users',Super_views.users,name='user-page'),
    path('manage_user',Super_views.manage_user,name='manage-user'),
    path('manage_user/<int:pk>',Super_views.manage_user,name='manage-user-pk'),
    path('save_user',Super_views.save_user,name='save-user'),
    path('delete_user/<int:pk>',Super_views.delete_user,name='delete-user'),
    path('view_user',Super_views.view_user,name='view-user'),
    path('view_user/<int:pk>',Super_views.view_user,name='view-user-pk'),
    #franchise management
    path('franchise',Super_views.franchise,name='franchise-page'),
    path('manage_franchise',Super_views.manage_franchise,name='manage-franchise'),
    path('manage_franchise/<int:pk>',Super_views.manage_franchise,name='manage-franchise-pk'),
    path('save_franchise',Super_views.save_franchise,name='save-franchise'),
    path('delete_franchise/<int:pk>',Super_views.delete_franchise,name='delete-franchise'),
    path('view_franchise',Super_views.view_franchise,name='view-franchise'),
    path('view_franchise/<int:pk>',Super_views.view_franchise,name='view-franchise-pk'),
    path('update_status/<int:pk>',Super_views.update_status,name='update-status'),
    path('update_user_status',Super_views.update_user_status,name='update-user-status'),
    path('update_password/<int:pk>',Super_views.update_password,name='update-password'),
    path('update_password_franchise/<int:pk>',Super_views.update_password_franchise,name='update-password_franchise'),
    path('update_password_franchise',Super_views.update_password_franchise,name='update-password_franchise'),
    #vendor management
    path('vendor',Super_views.vendor,name='vendor-page'),
    path('manage_vendor',Super_views.manage_vendor,name='manage-vendor'),
    path('manage_vendor/<int:pk>',Super_views.manage_vendor,name='manage-vendor-pk'),
    path('save_vendor',Super_views.save_vendor,name='save-vendor'),
    path('delete_vendor/<int:pk>',Super_views.delete_vendor,name='delete-vendor'),
    path('view_vendor',Super_views.view_vendor,name='view-vendor'),
    path('view_vendor/<int:pk>',Super_views.view_vendor,name='view-vendor-pk'),
    path('update_password_vendor/<int:pk>',Super_views.update_password_vendor,name='update-password_vendor'),
    path('update_password_vendor',Super_views.update_password_vendor,name='update-password_vendor'),
    
    #rider management
    path('rider',Super_views.rider,name='rider-page'),
    path('manage_rider',Super_views.manage_rider,name='manage-rider'),
    path('manage_rider/<int:pk>',Super_views.manage_rider,name='manage-rider-pk'),
    path('save_rider',Super_views.save_rider,name='save-rider'),
    path('delete_rider/<int:pk>',Super_views.delete_rider,name='delete-rider'),
    path('view_rider',Super_views.view_rider,name='view-rider'),
    path('view_rider/<int:pk>',Super_views.view_rider,name='view-rider-pk'),
    path('update_password_rider/<int:pk>',Super_views.update_password_rider,name='update-password_rider'),
    path('update_password_rider',Super_views.update_password_rider,name='update-password_rider'),
    #product management
    path('products',Super_views.products,name='product-page'),
    path('manage_product',Super_views.manage_product,name='manage-product'),
    path('manage_product/<int:pk>',Super_views.manage_product,name='manage-product-pk'),
    path('view_product',Super_views.view_product,name='view-product'),
    path('view_product/<int:pk>',Super_views.view_product,name='view-product-pk'),
    path('save_product',Super_views.save_product,name='save-product'),
    path('delete_product/<int:pk>',Super_views.delete_product,name='delete-product'),
    path('save_productpurchase',Super_views.save_productpurchase,name='save-productpurchase'),
    path('view_productpurchase',Super_views.view_productpurchase,name='view-productpurchase'),
    path('view_productpurchase/<int:pk>',Super_views.view_productpurchase,name='view-productpurchase-pk'),
    path('manage_productpurchase',Super_views.manage_productpurchase,name='manage-productpurchase'), 
    path('manage_productpurchase/<int:pk>',Super_views.manage_productpurchase,name='manage-productpurchase-pk'),
    path('delete_productpurchase/<int:pk>',Super_views.delete_productpurchase,name='delete-productpurchase'),
    path('reciepts_productpurchase',Super_views.reciepts_productpurchase,name='reciepts_productpurchase'),
    path('manage_stockin/<int:pid>',Super_views.manage_stockin,name='manage-stockin-pid'),
    path('manage_stockin/<int:pid>/<int:pk>',Super_views.manage_stockin,name='manage-stockin-pid-pk'),
    path('save_stockin',Super_views.save_stockin,name='save-stockin'),
    path('delete_stockin/<int:pk>',Super_views.delete_stockin,name='delete-stockin'),
    path('fetch-contact', Super_views.fetch_contact, name='fetch-contact'),
    #category management
    path('categories',Super_views.price,name='price-page'),
    path('manage_price',Super_views.manage_price,name='manage-price'),
    path('manage_price/<int:pk>',Super_views.manage_price,name='manage-price-pk'),
    path('view_price/<int:pk>',Super_views.view_price,name='view-price-pk'),
    path('save_price',Super_views.save_price,name='save-price'),
    path('delete_price/<int:pk>',Super_views.delete_price,name='delete-price'),
    path('update_status_prices/<int:pk>',Super_views.update_status_prices,name='update-status_prices'),
    path('update_prices_status',Super_views.update_prices_status,name='update-prices-status'),
    #order management
    path('laundries',Super_views.laundries,name='laundry-page'),
    path('manage_laundry',Super_views.manage_laundry,name='manage-laundry'), 
    path('manage_laundry/<int:pk>',Super_views.manage_laundry,name='manage-laundry-pk'),
    path('view_laundry',Super_views.view_laundry,name='view-laundry'),
    path('view_laundry/<int:pk>',Super_views.view_laundry,name='view-laundry-pk'),
    path('save_laundry',Super_views.save_laundry,name='save-laundry'),
    path('delete_laundry/<int:pk>',Super_views.delete_laundry,name='delete-laundry'),
    path('update_status_laundry/<int:pk>',Super_views.update_status_laundry,name='update-status_laundry'),
    path('update_laundry_status_laundry',Super_views.update_laundry_status_laundry,name='update-laundry-status_laundry'),
    #staffs
    path('staffs',Super_views.staffs,name='staffs-page'),
    path('manage_staffs',Super_views.manage_staffs,name='manage-staffs'),
    path('manage_staffs/<int:pk>',Super_views.manage_staffs,name='manage-staffs-pk'),
    path('save_staffs',Super_views.save_staffs,name='save-staffs'),
    path('delete_staffs/<int:pk>',Super_views.delete_staffs,name='delete-staffs'),
    path('view_staffs',Super_views.view_staffs,name='view-staffs'),
    path('view_staffs/<int:pk>',Super_views.view_staffs,name='view-staffs-pk'),
    #report
    path('daily_report',Super_views.daily_report,name='daily-report'),
    path('daily_report/<str:date>',Super_views.daily_report,name='daily-report-date'),
    path('report_view',Super_views.report_view,name='report_view'),
    # tickets
    path('tickets',Super_views.tickets,name='tickets'),
    path('list',Super_views.list,name='list'),
    path('plist',Super_views.plist,name='plist'),
    path('allcomplaints',Super_views.allcomplaints,name='allcomplaints'),
    path('solved',Super_views.solved,name='solved'),
    # CCTV==admin
    path('CCTV_list', Super_views.CCTV_list, name='CCTV_list'),
    path('CCTV_delete/<str:tid>',Super_views.CCTV_delete,name='CCTV_delete'),
    #coupon management
    path('coupon',Super_views.coupon,name='coupon-page'),
    path('manage_coupon',Super_views.manage_coupon,name='manage-coupon'), 
    path('manage_coupon/<int:pk>',Super_views.manage_coupon,name='manage-coupon-pk'),
    path('save_coupon',Super_views.save_coupon,name='save-coupon'),
    
    path('delete_coupon/<int:pk>',Super_views.delete_coupon,name='delete-coupon'),
    path('view_coupon',Super_views.view_coupon,name='view-coupon'),
    path('view_coupon/<int:pk>',Super_views.view_coupon,name='view-coupon-pk'),
    path('apply_coupon_page',Super_views.apply_coupon_page,name='coupon-apply-page'),
    path('apply_coupon',Super_views.apply_coupon,name='apply-coupon'),
    #banner management
    path('banner_page',Super_views.banner_page,name='banner-page'),
    path('manage_banner',Super_views.manage_banner,name='manage-banner'), 
    path('manage_banner/<int:pk>',Super_views.manage_banner,name='manage-banner-pk'),
    path('save_banner',Super_views.save_banner,name='save-banner'),
    path('save_banner',Super_views.save_banner,name='save-banner'),
    path('delete_banner/<int:pk>',Super_views.delete_banner,name='delete-banner'),
    path('view_banner/<int:pk>',Super_views.view_banner,name='view-banner-pk'),
    #Contact us
    path('contact',Super_views.contact,name='contact-page'),
    path('manage_contact',Super_views.manage_contact,name='manage-contact'), 
    path('manage_contact/<int:pk>',Super_views.manage_contact,name='manage-contact-pk'),
    path('save_contact',Super_views.save_contact,name='save-contact'),
    path('save_contact',Super_views.save_contact,name='save-contact'),
    # path('delete_contact/<int:pk>',Super_views.delete_contact,name='delete-contact'),

    # Notifications
    path('notifications', Super_views.admin_notifications_view, name='notifications'),
    path('mark_notification_read', Super_views.mark_notification_read, name='mark-notification-read'),
    # path('all-notifications/', Super_views.all_notifications, name='all-notifications'),
    path('inbox/<int:notification_id>/',Super_views.inbox_convo, name='inbox_convo'),


    # timeslot
    path('timeslot',Super_views.timeslot,name='timeslot'),
    path('get_timeslots/', Super_views.get_timeslots, name='get_timeslots'),
    path('save_timeslots/', Super_views.save_timeslots, name='save_timeslots'),

    #Franchise_views
    path('franchise/', Franchise_views.franchise, name='franchise'),
    # path('login_user_franchise',Franchise_views.login_user_franchise,name='login_user-franchise'),

    #Profile management
    path('profile_franchise',Franchise_views.profile_franchise,name='profile-page_franchise'),
    # path('update_password',Franchise_views.update_password,name='update-password'),
    path('update_profile_franchise',Franchise_views.update_profile_franchise,name='update-profile_franchise'),
    # path('franchisepage/', Franchise_views.franchise_page, name='franchisepage'),
    #user management
    path('users_franchise',Franchise_views.users_franchise,name='user-page_franchise'),
    path('manage_user_franchise',Franchise_views.manage_user_franchise,name='manage-user_franchise'),
    path('manage_user_franchise/<int:pk>',Franchise_views.manage_user_franchise,name='manage-user_franchise-pk'),
    path('save_user_franchise',Franchise_views.save_user_franchise,name='save-user_franchise'),
    path('delete_user_franchise/<int:pk>',Franchise_views.delete_user_franchise,name='delete-user_franchise'),
    path('view_user_franchise',Franchise_views.view_user_franchise,name='view-user_franchise'),
    path('view_user_franchise/<int:pk>',Franchise_views.view_user_franchise,name='view-user_franchise-pk'),
    #vendor management
    path('vendor_franchise',Franchise_views.vendor_franchise,name='vendor-page_franchise'),
    path('manage_vendor_franchise',Franchise_views.manage_vendor_franchise,name='manage-vendor_franchise'),
    path('manage_vendor_franchise/<int:pk>',Franchise_views.manage_vendor_franchise,name='manage-vendor_franchise-pk'),
    path('save_vendor_franchise',Franchise_views.save_vendor_franchise,name='save-vendor_franchise'),
    path('delete_vendor_franchise/<int:pk>',Franchise_views.delete_vendor_franchise,name='delete-vendor_franchise'),
    path('view_vendor_franchise',Franchise_views.view_vendor_franchise,name='view-vendor_franchise'),
    path('view_vendor_franchise/<int:pk>',Franchise_views.view_vendor_franchise,name='view-vendor_franchise-pk'),
    path('update_password_vendor_franchise/<int:pk>',Franchise_views.update_password_vendor_franchise,name='update-password_vendor_franchise'),
    path('update_password_vendor_franchise',Franchise_views.update_password_vendor_franchise,name='update-password_vendor_franchise'),
    #rider management
    path('rider_franchise',Franchise_views.rider_franchise,name='rider-page_franchise'),
    path('manage_rider_franchise',Franchise_views.manage_rider_franchise,name='manage-rider_franchise'),
    path('manage_rider_franchise/<int:pk>',Franchise_views.manage_rider_franchise,name='manage-rider_franchise-pk'),
    path('save_rider_franchise',Franchise_views.save_rider_franchise,name='save-rider_franchise'),
    path('delete_rider_franchise/<int:pk>',Franchise_views.delete_rider_franchise,name='delete-rider_franchise'),
    path('view_rider_franchise',Franchise_views.view_rider_franchise,name='view-rider_franchise'),
    path('view_rider_franchise/<int:pk>',Franchise_views.view_rider_franchise,name='view-rider_franchise-pk'),
    path('update_password_rider_franchise/<int:pk>',Franchise_views.update_password_rider_franchise,name='update-password_rider_franchise'),
    path('update_password_rider_franchise',Franchise_views.update_password_rider_franchise,name='update-password_rider_franchise'),
    #category management
    path('categories_franchise',Franchise_views.price_franchise,name='price-page_franchise'),
    path('view_price_franchise/<int:pk>',Franchise_views.view_price_franchise,name='view-price_franchise-pk'),
    #Product managemnt
    path('products_all',Franchise_views.products_all,name='products-page_all'),
    path('view_product_all',Franchise_views.view_product_all,name='view-products_all'),
    path('view_product_all/<int:pk>',Franchise_views.view_product_all,name='view-products_all-pk'),
    #Product in stock
    path('products_franchise',Franchise_views.products_franchise,name='product-page_franchise'),
    path('manage_product_franchise',Franchise_views.manage_product_franchise,name='manage-product_franchise'),
    path('manage_product_franchise/<int:pk>',Franchise_views.manage_product_franchise,name='manage-product_franchise-pk'),
    path('save_product_franchise',Franchise_views.save_product_franchise,name='save-product_franchise'),
    path('view_productsfranchise',Franchise_views.view_productsfranchise,name='view-productsfranchise'),
    path('view_productsfranchise/<int:pk>',Franchise_views.view_productsfranchise,name='view-productsfranchise-pk'),
    path('delete_product_franchise/<int:pk>',Franchise_views.delete_product_franchise,name='delete-product_franchise'),
    path('manage_stockin_franchise/<int:pid>',Franchise_views.manage_stockin_franchise,name='manage-stockin_franchise-pid'),
    path('manage_stockin_franchise/<int:pid>/<int:pk>',Franchise_views.manage_stockin_franchise,name='manage-stockin_franchise-pid-pk'),
    path('save_stockin_franchise',Franchise_views.save_stockin_franchise,name='save-stockin_franchise'),
    path('manage_usedproduct',Franchise_views.manage_usedproduct,name='manage-usedproduct'), 
    path('manage_usedproduct/<int:pk>',Franchise_views.manage_usedproduct,name='manage-usedproduct-pk'),
    path('delete_stockin_franchise/<int:pk>',Franchise_views.delete_stockin_franchise,name='delete-stockin_franchise'),
    path('manage_stockout_franchise/<int:pid>',Franchise_views.manage_stockout_franchise,name='manage-stockout_franchise-pid'),
    path('manage_stockout_franchise/<int:pid>/<int:pk>',Franchise_views.manage_stockout_franchise,name='manage-stockout_franchise-pid-pk'),
    path('save_stockout_franchise',Franchise_views.save_stockout_franchise,name='save-stockout_franchise'),
    path('delete_stockout_franchise/<int:pk>',Franchise_views.delete_stockout_franchise,name='delete-stockout_franchise'),
    path('fetch-price_franchise', Franchise_views.fetch_price_franchise, name='fetch-price_franchise'),

    #staff management
    path('staffs_franchise',Franchise_views.staffs_franchise,name='staffs-page_franchise'),
    path('manage_staffs_franchise',Franchise_views.manage_staffs_franchise,name='manage-staffs_franchise'),
    path('manage_staffs_franchise/<int:pk>',Franchise_views.manage_staffs_franchise,name='manage-staffs_franchise-pk'),
    path('save_staffs_franchise',Franchise_views.save_staffs_franchise,name='save-staffs_franchise'),
    path('delete_staffs_franchise/<int:pk>',Franchise_views.delete_staffs_franchise,name='delete-staffs_franchise'),
    path('view_staffs_franchise',Franchise_views.view_staffs_franchise,name='view-staffs_franchise'),
    path('view_staffs_franchise/<int:pk>',Franchise_views.view_staffs_franchise,name='view-staffs_franchise-pk'),

    # path('attendance', Franchise_views.attendance_staff, name='attendance'),
    # # path('daily_report',Franchise_views.daily_report,name='daily-report'),
    # path('attendance/<str:date>',Franchise_views.attendance_staff,name='attendance-date'),
    path('attendance_class',Franchise_views.attendance_class,name='attendance-class'),
    # path('attendance',Franchise_views.attendance,name='attendance-page'),
    # path('attendance',Franchise_views.attendance,name='attendance-page'),
    path(r'attendance_class/<str:date>',Franchise_views.attendance_class,name='attendance_class-date'),
    path('save_attendance',Franchise_views.save_attendance,name='save-attendance'),
    path('save_attendance',Franchise_views.save_attendance,name='save-attendance'),
    path('manage_attendance_franchise',Franchise_views.manage_attendance_franchise,name='manage-attendance_franchise'),
    path('manage_attendance_franchise/<int:pk>',Franchise_views.manage_attendance_franchise,name='manage-attendance_franchise-pk'),
    path('delete_attendance_franchise/<int:pk>',Franchise_views.delete_attendance_franchise,name='delete-attendance_franchise'),
    #franchise order managemnet
    path('laundries_franchise',Franchise_views.laundries_franchise,name='laundry-page_franchise'),
    path('manage_laundry_franchise',Franchise_views.manage_laundry_franchise,name='manage-laundry_franchise'), 
    path('pickup',Franchise_views.manage_laundry_franchise_pickup,name='manage-laundry_franchise_pickup'), 
    path('pickup/<int:pk>',Franchise_views.manage_laundry_franchise_pickup,name='manage-laundry_franchise_pickup-pk'), 
    path('manage_laundry_franchise/<int:pk>',Franchise_views.manage_laundry_franchise,name='manage-laundry_franchise-pk'),
    path('view_laundry_franchise',Franchise_views.view_laundry_franchise,name='view-laundry_franchise'),
    path('view_laundry_franchise/<int:pk>',Franchise_views.view_laundry_franchise,name='view-laundry_franchise-pk'),
    path('save_laundry_franchise',Franchise_views.save_laundry_franchise,name='save-laundry_franchise'),
    path('save_laundry_franchise_pickup',Franchise_views.save_laundry_franchise_pickup,name='save-laundry_franchise_pickup'),
    path('delete_laundry_franchise/<int:pk>',Franchise_views.delete_laundry_franchise,name='delete-laundry_franchise'),
    path('update_transaction_form/<int:pk>',Franchise_views.update_transaction_form,name='transacton-update-status'),
    path('update_transaction_status',Franchise_views.update_transaction_status,name='update-laundry-status'),
    path('reciepts_franchise',Franchise_views.reciepts_franchise,name='reciepts_franchise'),
    path('view_reciepts_franchise',Franchise_views.view_reciepts_franchise,name='view-reciepts_franchise'),
    path('view_reciepts_franchise/<int:pk>',Franchise_views.view_reciepts_franchise,name='view-reciepts_franchise-pk'),
    path('fetch-contact_franchise', Franchise_views.fetch_contact_franchise, name='fetch-contact_franchise'),
    #franchise vendor order managemnet
    path('laundries_franchise_vendor',Franchise_views.laundries_franchise_vendor,name='laundry-page_franchise_vendor'),
    path('manage_laundry_franchise_vendor',Franchise_views.manage_laundry_franchise_vendor,name='manage-laundry_franchise_vendor'), 
    path('manage_laundry_franchise_vendor/<int:pk>',Franchise_views.manage_laundry_franchise_vendor,name='manage-laundry_franchise_vendor-pk'),
    path('view_laundry_franchise_vendor',Franchise_views.view_laundry_franchise_vendor,name='view-laundry_franchise_vendor'),
    path('view_laundry_franchise_vendor/<int:pk>',Franchise_views.view_laundry_franchise_vendor,name='view-laundry_franchise_vendor-pk'),
    path('save_laundry_franchise_vendor',Franchise_views.save_laundry_franchise_vendor,name='save-laundry_franchise_vendor'),
    path('delete_laundry_franchise_vendor/<int:pk>',Franchise_views.delete_laundry_franchise_vendor,name='delete-laundry_franchise_vendor'),
    path('update_transaction_form/<int:pk>',Franchise_views.update_transaction_form,name='transacton-update-status'),
    path('update_transaction_status',Franchise_views.update_transaction_status,name='update-laundry-status'),
    path('reciepts_franchise_vendor',Franchise_views.reciepts_franchise_vendor,name='reciepts_franchise_vendor'),
    path('view_reciepts_franchise_vendor',Franchise_views.view_reciepts_franchise_vendor,name='view-reciepts_franchise_vendor'),
    path('view_reciepts_franchise_vendor/<int:pk>',Franchise_views.view_reciepts_franchise_vendor,name='view-reciepts_franchise_vendor-pk'),
     # barcode
    # path('scan_barcode', Franchise_views.barcode_scan_view, name='scan_barcode'),
    path('scan_barcode/<int:pk>', Franchise_views.barcode_scan_view, name='scan_barcode-pk'),
    path('process_barcode/', Franchise_views.process_barcode_view, name='process_barcode'),
    path('daily_report_franchise',Franchise_views.daily_report_franchise,name='daily-report_franchise'),
    path('daily_report_franchise/<str:date>',Franchise_views.daily_report_franchise,name='daily-report_franchise-date'),
    path('report_view_franchise',Franchise_views.report_view_franchise,name='report_view_franchise'),
    # b2c & pickup
    path('b2c_form',Franchise_views.b2c_form,name="b2c_form"),
    path('B2cview',Franchise_views.B2cview,name="B2cview"),
    # path('manage_B2c/<int:pk>',Franchise_views.manage_B2c,name='manage-B2c'),
    path('delete_B2c/<int:pk>',Franchise_views.delete_B2c,name='delete-B2c'),
    path('pickup_form',Franchise_views.pickup_form,name="pickup_form"),
    path('pickupview',Franchise_views.pickupview,name="pickupview"),
    path('delete_pickup/<int:pk>',Franchise_views.delete_pickup,name='delete-pickup'),
    # path('thank',Franchise_views.thank,name="thank"),
    # tickets
    path('tickets_franchise',Franchise_views.tickets_franchise,name='tickets_franchise'),
    path('list_franchise',Franchise_views.list_franchise,name='list_franchise'),
    path('plist_franchise',Franchise_views.plist_franchise,name='plist_franchise'),
    path('allcomplaints_franchise',Franchise_views.allcomplaints_franchise,name='allcomplaints_franchise'),
    path('solved_franchise',Franchise_views.solved_franchise,name='solved_franchise'),
    # API
    path('default-category/', Franchise_views.default_category, name='default_category'),
    path('get-laundrytypes/', Franchise_views.get_laundrytypes, name='get_laundrytypes'),
    # chat
    path('chat', Super_views.chat_admin, name='chat-super'),
    path('send/', Super_views.send_chat, name='chat-send-super'),
    path('renew/', Super_views.get_messages, name='chat-renew-super'),

    path('chat_franchise', Franchise_views.chat_franchise, name='chat-franchise'),
    path('send_franchise/', Franchise_views.send_chat_franchise, name='chat-send-franchise'),
    path('renew_franchise/', Franchise_views.get_messages_franchise, name='chat-renew-franchise'),
    # CCTV==franchise
    path('CCTV_form', Franchise_views.CCTV_form, name='CCTV_form'),
    #coupon management
    path('coupon_franchise',Franchise_views.coupon_franchise,name='coupon_franchise-page'),
    path('manage_coupon_franchise',Franchise_views.manage_coupon_franchise,name='manage-coupon_franchise'), 
    path('manage_coupon_franchise/<int:pk>',Franchise_views.manage_coupon_franchise,name='manage-coupon_franchise-pk'),
    path('save_coupon_franchise',Franchise_views.save_coupon_franchise,name='save-coupon_franchise'),    
    path('delete_coupon_franchise/<int:pk>',Franchise_views.delete_coupon_franchise,name='delete-coupon_franchise'),
    path('view_coupon_franchise',Franchise_views.view_coupon_franchise,name='view-coupon_franchise'),
    path('view_coupon_franchise/<int:pk>',Franchise_views.view_coupon_franchise,name='view-coupon_franchise-pk'),
    # notifications

    # path('restock-request/',Franchise_views.restock_request_view, name='restock-request'),
    path('render_restock_modal/<int:pk>', Franchise_views.render_restock_request_modal, name='render-restock-modal'),
    path('send_restock_request/', Franchise_views.send_restock_request, name='send-restock-request'),
    path('send-cancel-request/', Franchise_views.send_cancel_request, name='send-cancel-request'),
    
    # notification from admin
    path('franchise-notifications', Franchise_views.franchise_notifications_view, name='franchise-notifications'),
    path('franchise-mark_notification_read', Franchise_views.franchise_mark_notification_read, name='franchise-mark-notification-read'),
    # path('all-notifications/', Franchise_views.all_notifications, name='all-notifications'),
    path('franchise-inbox/<int:notification_id>/',Franchise_views.franchise_inbox_convo, name='franchise-inbox_convo'),


        # timeslot
    path('timeslot_franchise',Franchise_views.timeslot_franchise,name='timeslot_franchise'),
    path('get_timeslots_franchise/', Franchise_views.get_timeslots_franchise, name='get_timeslots_franchise'),
    path('save_timeslots_franchise/', Franchise_views.save_timeslots_franchise, name='save_timeslots_franchise'),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)