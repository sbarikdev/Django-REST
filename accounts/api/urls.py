
from django.urls import path, include
from .views import *

urlpatterns = [
    path('login', LoginAPIView.as_view(), name='login_api'),
]
