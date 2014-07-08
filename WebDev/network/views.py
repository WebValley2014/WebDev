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
from forms import *
from WebDev.utils import *
import hashlib

inputName = "Classification"

@login_required(login_url="/login")
def network(request, pip_id):
    try:
        pip = Pipeline.objects.get(pip_id=pip_id)
        result = Results.objects.get(pip_id=pip, process_name='processing')
    except:
        return HttpResponse('Bad Request: Pipline %s does not exist.' % (pip_id,))
    return HttpResponse("FILE: %s" % (result.filepath,))

@login_required(login_url="/login")
def network_redirect(request):
    return HttpResponseRedirect("upload/")

def step2(request):
    return render(request, 'network/tuttook.html')

@login_required(login_url="/login")
def upload_network(request):
    global inputName
    form_error = False
    form = NUploadFileForm()
    if request.POST:
        print request.FILES
        if request.FILES:
            try:
                fileData = request.FILES['fileData']
                fileLabel = request.FILES['fileLabel']
                fileSamples = request.FILES['fileSamples']
                fileFeature = request.FILES['fileFeature']
                fileRank = request.FILES['fileRank']
                fileMetrics = request.FILES['fileMetrics']
            except:
                messages.error(request, "Insert the correct files")
                form_error = True

            if not form_error:
                li = [fileData.name, fileLabel.name, fileSamples.name, fileFeature.name, fileRank.name, fileMetrics.name]
                if not different(li):
                    form_error = True
                    messages.error(request, "Some files with the same name")
            if not form_error:
                if checkExtension(fileData, 'txt') and checkExtension(fileLabel, 'txt') and checkExtension(fileSamples, 'txt') and checkExtension(fileFeature, 'txt') and checkExtension(fileRank, 'txt') and checkExtension(fileMetrics, 'txt'):
                    p = Pipeline(pip_name='network', pip_id=hashlib.md5(str(uuid.uuid1())).hexdigest(),
                                 started=timezone.now(), description='', owner=request.user)
                    p.save()

                    handle_uploaded_file(p,fileData,inputName)
                    handle_uploaded_file(p,fileLabel,inputName)
                    handle_uploaded_file(p,fileSamples,inputName)
                    handle_uploaded_file(p,fileFeature,inputName)
                    handle_uploaded_file(p,fileRank,inputName)
                    handle_uploaded_file(p,fileMetrics,inputName)
                    return HttpResponse('/network/step2/')
                else:
                    messages.error(request, "File type incorrect")
        else:
            messages.error(request, "Insert the correct files")
        return HttpResponse('/network/upload/')

    # Old files
    oldFiles = Results.objects.filter(process_name=inputName, owner=request.user)
    oldFiles = oldFiles.order_by('-id')

    tabFile = []
    for i in range(0, len(oldFiles), 6):
        tabFile.append(files(oldFiles[i], oldFiles[i+1], oldFiles[i+2], oldFiles[i+3], oldFiles[i+4], oldFiles[i+5]))

    return render(request, 'network/network.html', {'tabFile': tabFile, 'file_exist': (len(oldFiles)>0)})
'''
        messages.warning(request, 'No uploaded file')
    if request.POST and request.FILES:
        if checkExtension(request.FILES['fileData'], 'txt') and checkExtension(request.FILES['fileLabel'], 'txt') and checkExtension(request.FILES['fileSamples'], 'txt') and checkExtension(request.FILES['fileFeature'], 'txt') and checkExtension(request.FILES['fileRank'], 'txt'):
            form = NUploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                p = Pipeline(pip_name='network', pip_id=str(uuid.uuid1()), started=timezone.now(), description='', owner=request.user)
                p.save()
                # FIXME: to do: check on file name (maybe in js?)
                handle_uploaded_file(p,request.FILES['fileData'])
                handle_uploaded_file(p,request.FILES['fileLabel'])
                handle_uploaded_file(p,request.FILES['fileSamples'])
                handle_uploaded_file(p,request.FILES['fileFeature'])
                handle_uploaded_file(p,request.FILES['fileRank'])
                return render(request, 'network/tuttook.html')
        else:
            messages.error(request, 'Wrong file type')
    oldFiles = Results.objects.filter(process_name='network', owner=request.user)
    oldFiles = oldFiles.order_by('-id')
    return render(request, 'network/network.html', {'oldFiles': oldFiles, 'file_exist': (len(oldFiles)>0)})
    '''
'''
@login_required(login_url="/login")
def upload_network(request):
    form_error, ex_error = False, False
    #IF FILE UPLOADED
    if request.POST:
        if request.FILES:
            try:
                file_sff = request.FILES['file_sff']
                file_map = request.FILES['file_map']
            except:
                messages.error(request, "Insert the correct file")
                form_error = True
            if not form_error:
                if checkExtension(file_sff, 'sff') and checkExtension(file_map, 'map'):
                    p = Pipeline(pip_name='network', pip_id=hashlib.md5(str(uuid.uuid1())).hexdigest(),
                                 started=timezone.now(), description='', owner=request.user)
                    p.save()
                    handle_uploaded_file(p, file_sff)
                    handle_uploaded_file(p, file_map)
                    return render(request, 'network/tuttook.html')
                else:
                    messages.error(request, "File type incorrect")
        else:
            messages.error(request, "Insert the correct file")
        return HttpResponse('/network/upload/')

    # ELSE GENERATE THE FILE UPLOAD PAGE
    pre_file = Results.objects.filter(process_name='network', owner=request.user).order_by('-id')
    #Order the list
    final_file = pick_file_list(pre_file)
    if len(final_file) == 0:
        file_exist = False
    else:
        file_exist = True
    c = {
        'file_list': final_file,
        'file_exist': file_exist
    }
    return render(request, 'network/network.html', c)
'''


@login_required(login_url="/login")
def deleteFile(request, id1, id2, id3, id4, id5, id6):
    re = Results.objects.get(pk=int(id1))
    delete(re)
    re = Results.objects.get(pk=int(id2))
    delete(re)
    re = Results.objects.get(pk=int(id3))
    delete(re)
    re = Results.objects.get(pk=int(id4))
    delete(re)
    re = Results.objects.get(pk=int(id5))
    delete(re)
    re = Results.objects.get(pk=int(id6))
    delete(re)
    return HttpResponseRedirect('/network/upload')