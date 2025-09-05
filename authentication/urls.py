from django.contrib import admin
from django.urls import path, include
from authentication import views

urlpatterns = [
    path('', views.signin, name='signin'),
    path("signup", views.signup, name='signup'),
    path("signout", views.signout, name='signout'),
    path('password_reset', views.password_reset, name='password_reset'),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('delete_entry', views.delete_entry, name='delete_entry'),
]

