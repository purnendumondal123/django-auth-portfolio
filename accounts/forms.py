from django import forms
from django_recaptcha.fields import ReCaptchaField

class CaptchaForm(forms.Form):
    captcha = ReCaptchaField()