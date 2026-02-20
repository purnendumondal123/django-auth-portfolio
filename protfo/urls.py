from django.urls import path
from . import views

urlpatterns = [
    path('',views.Profo,{'template_name':'home.html', 'title': 'Home'}, name='home'),
    path('about/',views.Profo,{'template_name':'about.html', 'title': 'About'}, name='about'),
    path('contact/',views.Profo,{'template_name':'contact.html', 'title': 'Contact'}, name='contact'),
]
