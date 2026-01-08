from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_report, name='create_report'),
    path('create/user/<int:user_id>/', views.create_report, name='create_user_report'),
    path('create/listing/<uuid:listing_id>/', views.create_report, name='create_listing_report'),
]

