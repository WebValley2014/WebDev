from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import  HttpResponse
# Create your views here.

@login_required(login_url="/login")
def classification(request):
    return HttpResponse("ok")