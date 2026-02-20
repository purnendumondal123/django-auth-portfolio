from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import TempUser
from fullauth.settings import EMAIL_HOST_USER 
import random
from django.contrib import messages 
from . forms import CaptchaForm


# Create your views here.
def Register(request):
    if request.method=="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('conf-password')
        
        if pass1==pass2:
            if TempUser.objects.filter(email=email).exists() or User.objects.filter(email=email).exists():
                return render(request, 'register.html',{'msg':'Email already used', 'color':'danger', 'disp_email':'block', 'name':name})

            otp = random.randint(1000,9999)
            TempUser.objects.create(name=name, email=email, password=pass1, otp=otp)

            send_mail(
                subject='Your OTP code',
                message=f'Your OTP is {otp}',
                from_email= EMAIL_HOST_USER,
                recipient_list=[email]
            )
            request.session['email']= email
            return redirect('otp')
        else:
            context ={
                'pasmsg':"Confirm-Password is not match",
                'color':'danger',
                'disp_pass':'block',
                'name': name,
                'email': email,
            }
            return render(request, 'register.html', context)
        
    return render(request, 'register.html')
        
        
def otp_verify(request):
    email = request.session.get('email')
    if not email:
        return redirect('register')
    temp_user = TempUser.objects.filter(email=email).first()
    
    if request.method=="POST":
        otp_input = request.POST.get('otp')
        if temp_user and temp_user.otp==otp_input:
            User.objects.create_user(
                username= email.split('@')[0]+ str(random.randint(10,99)),
                email=email,
                password= temp_user.password,
                first_name=temp_user.name
            )
            # temp_user.delete()
            TempUser.objects.all().delete()
            messages.info(request,'OTP Verified user created')
            return redirect('login')
        return render(request, 'otp.html',{'message': 'Invalid OTP', 'class':'danger', 'email':email, 'display':'block'})
    return render(request,'otp.html',{'email':email})


def login_user(request):
    if request.method=="POST":
        captcha_form = CaptchaForm(request.POST)
        
        if not captcha_form.is_valid():
            return render(request, 'login.html', {
                'captcha_message': 'Captcha failed',
                'captcha_class': 'danger',
                'captcha_display': 'block'})
        
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request,'login.html',{'message':'User does not exist', 'class':'danger', 'display':'block'})
        
        user_auth= authenticate(request, username= user.username, password=password)

        if user_auth is not None:
            login(request, user_auth)
            return redirect('/protfo/')
        else:
            return render(request, 'login.html',{'email_message':'Invalid Pasword', 'email_class':'danger','email_display':'block','email': email})
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')