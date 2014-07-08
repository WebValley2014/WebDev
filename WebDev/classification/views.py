from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
import uuid
# Create your views here.

from forms import CLUploadFileForm
from WebDev.utils import *

@login_required(login_url="/login")
def classification(request, pip_id):
    try:
        pip = Pipeline.objects.get(pip_id=pip_id)
        result = Results.objects.get(pip_id=pip, process_name='processing')
    except:
        return HttpResponse('Bad Request: Pipline %s does not exist.' % (pip_id,))
    return HttpResponse("FILE: %s" % (result.filepath,))

@login_required(login_url="/login")
def classification_redirect(request):
    return HttpResponseRedirect("upload/")

@login_required(login_url="/login")
def upload_preProcessed(request):
    form = CLUploadFileForm()
    if not form.is_valid() and request.POST:
        messages.warning(request, 'No uploaded file')
    if request.POST and request.FILES:
        if checkExtension(request.FILES['file'], 'codes'):
            form = CLUploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                p = Pipeline(pip_name='classification', pip_id=str(uuid.uuid1()), started=timezone.now(), description='', owner=request.user)
                p.save()
                handle_uploaded_file(p,request.FILES['file'])
                return render(request, 'classification/tuttook.html')
        else:
            messages.error(request, 'Wrong file type')
    oldFiles = Results.objects.filter(process_name='classification', owner=request.user)
    oldFiles = oldFiles.order_by('-id')
    return render(request, 'classification/classification.html', {'oldFiles': oldFiles, 'file_exist': (len(oldFiles)>0)})

@login_required(login_url="/login")
def deleteFile(request, id):
    re = Results.objects.get(pk=id)
    if re.owner == request.user:
        delete(re)
    return HttpResponseRedirect('/class/upload')


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