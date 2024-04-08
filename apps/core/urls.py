from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.account import views as account_views
from apps.car_rental import views

urlpatterns = [
    # NOTE: Account
    path('login/', account_views.login_view, name='login'),
    path('register/', account_views.register_view, name='register'),
    path('logout/', account_views.logout_view, name='logout'),
    # NOTE: Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin-profile/', login_required(account_views.admin_profile_view), name='admin-profile'),
    path('table/', views.table_view, name='table-basic'),
    path('manage-agent/', views.manage_agent_view, name='manage-agent'),
    path('manage-customer/', views.manage_customer_view, name='manage-customer'),
    path('manage-agent/delete-agent/<int:pk>/', views.delete_agent_view, name='delete-agent'),
    path(
        'manage-customer/delete-customer/<int:pk>/',
        views.delete_customer_view,
        name='delete-customer',
    ),
    path('manage-car/', views.manage_car_view, name='manage-car'),
    path('manage-category/', views.manage_category_view, name='manage-category'),
    path('manage-rental/', views.manage_rental_view, name='manage-rental'),
    path('manage-payment/', views.manage_payment_view, name='manage-payment'),
    path('manage-car/edit-car/<int:pk>/', views.edit_car_view, name='edit-car'),
    path('manage-car/delete-car/<int:pk>/', views.delete_car_view, name='delete-car'),
    path(
        'manage-category/edit-category/<int:pk>/',
        views.edit_category_view,
        name='edit-category',
    ),
    path(
        'manage-category/delete-category/<int:pk>/',
        views.delete_category_view,
        name='delete-category',
    ),
    path(
        'manage-rental/edit-rental/<int:pk>/',
        views.edit_rental_view,
        name='edit-rental',
    ),
    path(
        'manage-rental/delete-rental/<int:pk>/',
        views.delete_rental_view,
        name='delete-rental',
    ),
    path(
        'manage-payment/delete-payment/<int:pk>/',
        views.delete_payment_view,
        name='delete-payment',
    ),
    # NOTE: Export
    path('export-agents/csv/', views.export_agents_csv, name='export-agents-csv'),
    path('export-agents/excel/', views.export_agents_excel, name='export-agents-excel'),
    path('export-customers/csv/', views.export_customers_csv, name='export-customers-csv'),
    path('export-customers/excel/', views.export_customers_excel, name='export-customers-excel'),
    path('export-cars/csv/', views.export_cars_csv, name='export-cars-csv'),
    path('export-cars/excel/', views.export_cars_excel, name='export-cars-excel'),
    path('export-rentals/csv/', views.export_rentals_csv, name='export-rentals-csv'),
    path('export-rentals/excel/', views.export_rentals_excel, name='export-rentals-excel'),
    # TODO: Clean Code
    path('icon-material/', views.icon_material_view, name='icon-material'),
    path('map-google/', views.map_google_view, name='map-google'),
    path('blank-page/', views.blank_view, name='blank-page'),
    path('not-found-404/', views.page_not_found_view, name='page-not-found'),
    # NOTE: Customer
    path('', views.home_view, name='home'),
    path('user-profile/', login_required(account_views.user_profile_view), name='user-profile'),
    path(
        'edit-user-profile/<int:pk>/',
        login_required(account_views.edit_user_profile_view),
        name='edit-user-profile',
    ),
    path('rental/<int:pk>/', login_required(views.rental_view), name='rental'),
    path('book-now/', views.book_now_view, name='book-now'),
    path(
        'rental/payment-receipt/<int:pk>/',
        views.payment_receipt_view,
        name='payment-receipt',
    ),
    path(
        'export-payment-to-pdf/<int:pk>/', views.export_payment_to_pdf, name='export-payment-to-pdf'
    ),
    path('error-page/', views.error_page_view, name='error-page'),
    path('about/', views.about_view, name='about'),
    path('service/', views.service_view, name='service'),
    path('portfolio/', views.portfolio_view, name='portfolio'),
    path('contact-us/', views.contact_view, name='contact'),
]
