from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def Profo(request, template_name, title):
    return render(request, template_name, {"title":title})