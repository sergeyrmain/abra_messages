from django.contrib import admin
from django.urls import path, include  # Import include for including app-level URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('messages.urls')),
]
