from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('register/',views.Register, name='register'),
    path('otp/',views.otp_verify, name='otp'),
    path('logout/', views.logout_user, name='logout')
]
