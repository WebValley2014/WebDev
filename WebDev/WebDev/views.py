from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from forms import UploadFileForm


def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def about_us(request):
    return render(request, 'about_us.html')
