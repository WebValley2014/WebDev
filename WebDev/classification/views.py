from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from WebDev.models import *
import os
from django.utils import timezone
import os, tempfile, zipfile
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
import mimetypes
from django.core.files import File
from django.utils.encoding import smart_str
# Create your views here.

from forms import CLUploadFileForm
from utils import handle_uploaded_file, download_file, check_owner

@login_required(login_url="/login")
def classification(request, p_id = ''):
    if(p_id == ''):
        return HttpResponseRedirect('upload')
    if not check_owner(request.user, p_id):
        return render(request, "error_owner.html")
    context = {
        'p_id': p_id
    }
    return render(request, 'classification/main.html', context)

@login_required(login_url="/login")
def upload_preProcessed(request):
    p = Pipeline(pip_name='classification', pip_id='', started=timezone.now(), description='', owner=request.user)
    p.save()
    form = CLUploadFileForm()
    if request.POST and request.FILES:
        form = CLUploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.user.username, p.pk, request.FILES['file'])
            return HttpResponseRedirect('/class/'+str(p.pk)+'/')
    return render(request, 'classification/classification.html')

@login_required(login_url="/login")
def download(request, p_id):

    #Generate the path file
    pip = Pipeline.objects.filter(id=int(p_id))
    download_path = os.path.join(settings.MEDIA_CLASSIFICATION_ROOT, str(pip[0].owner))
    download_path = os.path.join(download_path, str(pip[0].pk))
    download_path = os.path.join(download_path, 'file')

    #Retriv the download
    return download_file("file.txt", download_path)

def option(request, p_id):
    return render(request, 'classification/option.html', {'p_id': p_id})