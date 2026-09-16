from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:vehicle_id>/', views.create_booking, name='create_booking'),
    path('update/<int:booking_id>/', views.update_booking, name='update_booking'),
    path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('invoice/<int:booking_id>/', views.view_invoice, name='view_invoice'),
    path('rate/<int:booking_id>/', views.rate_service, name='rate_service'),
]
