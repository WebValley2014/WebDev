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
import hashlib
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

def step2(request):
    return render(request, 'classification/tuttook.html')

@login_required(login_url="/login")
def upload_preProcessed(request):
    form_error = False
    form = CLUploadFileForm()
    if request.POST:
        if request.FILES:
            try:
                file1 = request.FILES['file1']
                file2 = request.FILES['file2']
            except:
                messages.error(request, "Insert the correct files")
                form_error = True

            if not form_error:
                li = [file1.name, file2.name]
                if not different(li):
                    form_error = True
                    messages.error(request, "Some files with the same name")
            if not form_error:
                if checkExtension(file1, 'txt') and checkExtension(file2, 'txt'):
                    p = Pipeline(pip_name='Classification', pip_id=hashlib.md5(str(uuid.uuid1())).hexdigest(),
                                 started=timezone.now(), description='', owner=request.user)
                    p.save()

                    handle_uploaded_file(p,file1)
                    handle_uploaded_file(p,file2)
                    return HttpResponse('/class/step2/')
                else:
                    messages.error(request, "File type incorrect")
        else:
            messages.error(request, "Insert the correct files")
        return HttpResponse('/class/upload/')
    oldFiles = Results.objects.filter(process_name='Classification', owner=request.user)
    oldFiles = oldFiles.order_by('-id')
    return render(request, 'classification/classification.html', {'oldFiles': oldFiles, 'file_exist': (len(oldFiles)>0)})

'''
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
'''
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

    #Retrive the download
    return download_file("file.txt", download_path)

def option(request, p_id):
    return render(request, 'classification/option.html', {'p_id': p_id})