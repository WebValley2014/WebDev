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
from WebDev.store import *
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

#def step2(request, pip_id):
#    return render(request, 'network/tuttook.html')

@login_required(login_url="/login")
def upload_network(request):
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

                    handle_uploaded_file(p,fileData,inputName,'nt_data')
                    handle_uploaded_file(p,fileLabel,inputName, 'nt_label')
                    handle_uploaded_file(p,fileSamples,inputName, 'nt_samples')
                    handle_uploaded_file(p,fileFeature,inputName, 'nt_feature')
                    handle_uploaded_file(p,fileRank,inputName, 'nt_rank')
                    handle_uploaded_file(p,fileMetrics,inputName, 'nt_metrics')
                    return HttpResponse('/network/option/' + p.pip_id)
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
        tabFile.append(files(oldFiles[i], oldFiles[i+1], oldFiles[i+2], oldFiles[i+3], oldFiles[i+4], oldFiles[i+5], oldFiles[i].pip_id.pip_id))

    return render(request, 'network/network.html', {'tabFile': tabFile, 'file_exist': (len(oldFiles)>0)})


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

@login_required(login_url="/login")
def start_network(request, pip_id):
    pip = Pipeline.objects.get(pip_id=pip_id)
    file_nt_data = Results.objects.get(pip_id=pip, process_name=inputName, filetype='nt_data')
    file_nt_label = Results.objects.get(pip_id=pip, process_name=inputName, filetype='nt_label')
    file_nt_samples = Results.objects.get(pip_id=pip, process_name=inputName, filetype='nt_samples')
    file_nt_feature = Results.objects.get(pip_id=pip, process_name=inputName, filetype='nt_feature')
    file_nt_rank = Results.objects.get(pip_id=pip, process_name=inputName, filetype='nt_rank')
    file_nt_metrics = Results.objects.get(pip_id=pip, process_name=inputName, filetype='nt_metrics')
    inputFiles = {'fileData': file_nt_data.filepath, 'fileLabel': file_nt_label.filepath, 'fileSamples': file_nt_samples.filepath,
                  'fileFeature': file_nt_feature.filepath, 'fileRank': file_nt_rank.filepath, 'fileMetrics': file_nt_metrics.filepath}
    preproc_id = settings.APP.send_task("network_task", **inpu tFiles)
    store_before_celery(pip_id, inputFiles, preproc_id.id, "Network")
    return HttpResponseRedirect("/network/processing/" + preproc_id.id + "/")

def processing(request, task_id):
    result = settings.APP.AsyncResult(task_id)
    if result.ready():
        return HttpResponseRedirect('/network/processing_finish/%s/' % (task_id,))
    else:
        return HttpResponse(result.status)

def processing_finish(request, task_id):
    result = settings.APP.AsyncResult(task_id)
    if result.ready():
        r = result.get()
        rp = RunningProcess.objects.get(task_id=task_id)
        if store_after_celery(rp, r, 'txt'):
            return HttpResponse('OK')
        else:
            return HttpResponse('Error')
    return HttpResponseRedirect('/network/processing/%s/' % (task_id,))

@login_required(login_url="/login")
def option(request, pip_id):
    return render(request, 'network/option.html', {'pip_id': pip_id})

#@login_required(login_url="/login")
#def showResults(request):