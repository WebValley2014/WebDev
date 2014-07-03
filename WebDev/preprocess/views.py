from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import  HttpResponse
# Create your views here.

from forms import PPUploadFileForm
from utils import handle_uploaded_file

@login_required(login_url="/login")
def preprocess(request):
    form = PPUploadFileForm()
    if request.POST and request.FILES:
        form = PPUploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return render(request, 'preprocess/tuttook.html')
        else:
            return render(request, 'preprocess/preprocess.html')
    return render(request, 'preprocess/preprocess.html')
