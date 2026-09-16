from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/owner/', views.owner_dashboard, name='owner_dashboard'),
    path('dashboard/advisor/', views.advisor_dashboard, name='advisor_dashboard'),
    path('dashboard/mechanic/', views.mechanic_dashboard, name='mechanic_dashboard'),
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),
    path('ai-mechanic/', views.ai_mechanic_page, name='ai_mechanic'),
    path('ai-mechanic/chat/', views.ai_mechanic_chat, name='ai_chat'),
]
