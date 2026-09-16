from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('vehicle/add/', views.add_vehicle, name='add_vehicle'),
]
