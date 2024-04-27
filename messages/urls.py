from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from .views import message_list, message_detail, register, unread_message_list

urlpatterns = [
    path('messages/', message_list, name='message_list'),
    path('messages/<int:pk>/', message_detail, name='message_detail'),
    path('message-list/', message_list, name='message_list'),
    path('register/', register, name='register'),
    path('api-token-auth/', ObtainAuthToken.as_view(), name='api_token_auth'),
    path('message-list/unread/', unread_message_list, name='unread_message_list'),
]
