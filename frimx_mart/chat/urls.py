from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('<uuid:thread_id>/', views.chat_detail, name='chat_detail'),
    path('start/<uuid:listing_id>/', views.start_chat, name='start_chat'),
    path('<uuid:thread_id>/send/', views.send_message, name='send_message'),
    path('<uuid:thread_id>/get/', views.get_messages, name='get_messages'),
    path('block/<int:user_id>/', views.block_user, name='block_user'),
]