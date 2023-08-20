"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    #Send Get with user_id to get completed bookings
    path('completed_bookings/<int:id>', completed_bookings_list),

    #Send Get with user_id to get pending bookings
    #Send Put with to add new bookings
    path('pending_bookings/<int:id>', pending_bookings_list),

    path('admin/', admin.site.urls),
    path('payment_methods/<int:payment_id>', payment_method_details),
    path('payment_methods/', payment_method_list),
    path('available_seats/<int:flight_id>', available_seat_list),
    path('', index),
    path('payment_methods/', payment_method_list),
    path('login/', login_view),
    path('register/', register_view),
    path('flight_schedules/', available_flights_view),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
