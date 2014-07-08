import datetime
import hashlib
from WebDev.models import *
from django.contrib.auth.decorators import login_required
import uuid
from forms import PPUploadFileForm
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from utils import pick_file_list
from django.shortcuts import HttpResponse
from WebDev.utils import *
from django.contrib import messages
from django.conf import settings
import os
import time


@login_required(login_url="/login")
def preprocess_redirect(request):
    return HttpResponseRedirect("upload/")


@login_required(login_url="/login")
def get_results(request, p):
    return HttpResponse("Ok")


@login_required(login_url="/login")
def upload(request):
    form_error, ex_error = False, False
    #IF FILE UPLOADED
    if request.POST:
        if request.FILES:
            try:
                file_sff = request.FILES['file_sff']
                file_map = request.FILES['file_map']
            except:
                messages.error(request, "Insert the correct file")
            if not form_error:
                if checkExtension(file_sff, 'sff') and checkExtension(file_map, 'map'):
                    p = Pipeline(pip_name='preprocess', pip_id=hashlib.md5(str(uuid.uuid1())).hexdigest(),
                                 started=timezone.now(), description='', owner=request.user)
                    print p
                    p.save()
                    handle_uploaded_file(p, file_sff)
                    handle_uploaded_file(p, file_map)
                    return HttpResponse('/preproc/celery/' + p.pip_id)
                else:
                    messages.error(request, "File type incorrect")
        else:
            messages.error(request, "Insert the correct file")

    # ELSE GENERATE THE FILE UPLOAD PAGE
    pre_file = Results.objects.filter(process_name='preprocess', owner=request.user).order_by('-id')
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
    return render(request, 'preprocess/upload.html', c)


@login_required(login_url="/login")
def deleteFile(request, id1, id2):
    # Delete the file
    re1 = Results.objects.get(id=int(id1))
    re2 = Results.objects.get(id=int(id2))
    if re1.owner == request.user:
        delete(re1)
    if re2.owner == request.user:
        delete(re2)
    return HttpResponseRedirect('/preproc/upload')


@login_required(login_url="/login")
def start_preprocess(request, pip_id, new_pip=0):
    pip = Pipeline.objects.get(pip_id=pip_id)
    file_sff = Results.objects.get(pip_id=pip, process_name='preprocess', filetype='sff')
    file_map = Results.objects.get(pip_id=pip, process_name='preprocess', filetype='map')

    preproc_id = settings.APP.send_task("prepro", (pip.pip_id, file_sff.filepath, file_map.filepath))

    input_data = {'file_map': file_map.filepath, 'file_sff': file_sff.filepath}
    store_before_celery(pip, input_data, preproc_id.id)

    return HttpResponseRedirect("/preproc/processing/" + preproc_id.id + "/")


@login_required(login_url='/login')
def processing(request, process_id):
    # Pick the results
    result = settings.APP.AsyncResult(process_id)
    return HttpResponse(result.status)

def processing_finish(request, pip_id, task_id):
    result = settings.APP.AsyncResult(task_id)
    while not result.ready():
        time.sleep(1)
    r = result.get()
    rp = RunningProcess.objects.get(task_id=task_id)
    if store_after_celery(rp, r):
        return HttpResponse('OK')
    else:
        return HttpResponse('Error')


@login_required(login_url='/login')
def statusPP(request):
    tList = RunningProcess.objects.filter(process_name='Preprocessing')
    listPending = []
    listOK = []
    for el in tList:
        if el.pip_id.owner==request.user:
            if(settings.APP.AsyncResult(el.task_id).status=='PENDING'):
                listPending.append(el)
            else:
                listOK.append(el)
    return render(request, 'preprocess/status.html', {'listPending': listPending, 'listOK': listOK})

# CELERY FUNCTION

def store_before_celery(pip_id, jinput, task_id):
    '''
    This Function Stores the running process and info related to the results to the database.
    Needs to be called directly after [variable]= celery.start_task()

    :param pip_id: pipeline ID from Pipeline model.
    :param jinput: Dictionary of Inputs
    :param task_id: taskid
    :return: RunningProcess Database
    '''
    pname= 'Preprocessing'
    rundb = RunningProcess(process_name=pname,
                           pip_id=pip_id,
                           inputs=jinput,
                           submitted=datetime.datetime.now(),
                           task_id=task_id,
                           )
    rundb.save()
    return True

def store_after_celery(rundb, task_ret):
    '''
    Run after Celery Task
    :param rundb: from store_before_celery
    :param task_ret:  return of the celery task
    :return: True
    '''

    tp = 'txt'
    rundb.started = task_ret.st
    rundb.finished = task_ret.ft

    resdb = Results(process_name=rundb.process_name,
                    task_id=rundb.task_id,
                    filepath=task_ret.funct.pathname,
                    filetype=tp,
                    filename=task_ret.funct.filename,
                    )
    resdb.save()
    return True
