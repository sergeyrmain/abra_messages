from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from .views import message_list, message_detail, register

urlpatterns = [
    # registration:
    path('register/', register, name='register'),
    # GET tokens:
    path('api-token-auth/', ObtainAuthToken.as_view(), name='api_token_auth'),
    # GET all messages and POST new message:
    path('messages/', message_list, name='message_list'),
    # GET (read) a single message and DELETE single a message:
    path('messages/<int:pk>/', message_detail, name='message_detail'),
]
