from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_dashboard, name='user_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('moderate-listings/', views.moderate_listings, name='moderate_listings'),
    path('approve-boost/<uuid:listing_id>/', views.approve_boost, name='approve_boost'),
]

