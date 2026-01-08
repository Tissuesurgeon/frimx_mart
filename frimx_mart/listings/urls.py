from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('listings/', views.listing_list, name='listing_list'),
    path('listings/<uuid:listing_id>/', views.listing_detail, name='listing_detail'),
    path('listings/create/', views.create_listing, name='create_listing'),
    path('listings/<uuid:listing_id>/edit/', views.edit_listing, name='edit_listing'),
    path('listings/<uuid:listing_id>/delete/', views.delete_listing, name='delete_listing'),
    path('listings/<uuid:listing_id>/sold/', views.mark_as_sold, name='mark_as_sold'),
    path('listings/<uuid:listing_id>/save/', views.save_listing, name='save_listing'),
    path('seller/<int:seller_id>/review/', views.create_review, name='create_review'),
]