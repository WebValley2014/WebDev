from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from WebDev.models import *
from django.utils import timezone
# Create your views here.

from forms import CLUploadFileForm
from utils import handle_uploaded_file

@login_required(login_url="/login")
def classification(request, p_id = ''):
    if(p_id == ''):
        return HttpResponseRedirect('upload')
    return HttpResponse(p_id)

@login_required(login_url="/login")
def upload_preProcessed(request):
    p = Pipeline(pip_name='Classification', pip_id='', started=timezone.now(), description='', owner=request.user)
    p.save()
    form = CLUploadFileForm()
    if request.POST and request.FILES:
        form = CLUploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.user.username, p.pk, request.FILES['file'])
            return render(request, 'classification/tuttook.html')
    return render(request, 'classification/classification.html')
