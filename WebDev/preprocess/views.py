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
from WebDev.store import *
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
    # IF FILE UPLOADED
    if request.POST:
        if request.FILES:
            try:
                file_txt = request.FILES['file_txt']
            except:
                print 'error'
            try:
                print str(request.FILES)
                length = int(request.POST.get("length"))
                file_sff = []
                file_map = []
                for i in range(length):
                    a = request.FILES['file_sff_%s' % (i,)]
                    b = request.FILES['file_map_%s' % (i,)]
                    file_sff.append(a)
                    file_map.append(b)
                #file_txt = request.FILES['file_txt']
            except:
                messages.error(request, "Insert the correct files")
                form_error = True
            print form_error
            if not form_error:
                for i in range(length):
                    if not checkExtension(file_sff[i], 'sff') or not checkExtension(file_map[i], 'map'):
                        ex_error = True
                if not checkExtension(file_txt, 'txt'):
                    ex_error = True
                print ex_error
                if not ex_error:
                    p = Pipeline(pip_name='preprocess', pip_id=hashlib.md5(str(uuid.uuid1())).hexdigest(),
                                 started=timezone.now(), description='', owner=request.user)
                    p.save()
                    #print str(p.pip_id)
                    print length
                    for i in range(length):
                        print i
                        handle_uploaded_file(p, file_sff[i], 'preprocess')
                        handle_uploaded_file(p, file_map[i], 'preprocess')
                    handle_uploaded_file(p, file_txt, 'processing', 'class')
                    print 'finish'
                    return HttpResponse('/preproc/celery/' + p.pip_id)
                else:
                    messages.error(request, "File type incorrect")
            else:
                messages.error(request, "Insert the correct files")
        else:
            messages.error(request, "Insert the files")
        return HttpResponse('/preproc/upload/')

    # ELSE GENERATE THE FILE UPLOAD PAGE
    try:
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
    except:
        c = {'file_list': [], 'file_exist': False}
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

    # preproc_id = settings.APP.send_task("tasks.add", (5, 10))


    input_data = {'file_map': file_map.filepath, 'file_sff': file_sff.filepath}
    print  'Salva su database prima che celery abbia finito'
    store_before_celery(pip, input_data, preproc_id.id, "processing")

    return HttpResponseRedirect("/preproc/processing/" + preproc_id.id + "/")


# @login_required(login_url='/login')
def processing(request, task_id):
    # Pick the results
    result = settings.APP.AsyncResult(task_id)
    print str(result.status)
    print str(settings.APP)
    if result.ready():
        return HttpResponseRedirect('/preproc/processing_finish/%s/' % (task_id,))
    else:
        return HttpResponse(result.status)


def processing_finish(request, task_id):
    print 'Chiamata'
    # Pick the results
    result = settings.APP.AsyncResult(task_id)
    if result.ready():
        r = result.get()
        rp = RunningProcess.objects.get(task_id=task_id)
        if store_after_celery(rp, r, 'txt'):
            return HttpResponse('OK')
        else:
            return HttpResponse('Error')
    return HttpResponseRedirect('/preproc/processing/%s/' % (task_id,))


@login_required(login_url='/login')
def statusPP(request):
    tList = RunningProcess.objects.filter(process_name='Preprocessing')
    listRunning = []
    listFaliur = []
    listPending = []
    listSuccess = []
    listRetry = []
    listStarted = []
    for el in tList:
        if el.pip_id.owner == request.user:
            status = settings.APP.AsyncResult(el.task_id).status
            if (status == 'PENDING'):
                listPending.append(el)
            if (status == 'STARTED'):
                listStarted.append(el)
            if (status == 'RETRY'):
                listRetry.append(el)
            if (status == 'SUCCESS'):
                listSuccess.append(el)
            if (status == 'RUNNING'):
                listRunning.append(el)
            else:
                listFaliur.append(el)
            context = {
            'listPending': listPending,
            'listStarted': listStarted,
            'listRetry': listRetry,
            'listSuccess': listSuccess,
            'listRunning': listRunning,
            'listFaliur': listFaliur,

            }
    return render(request, 'preprocess/status.html', context)
    tList = RunningProcess.objects.filter(process_name='Preprocessing')
    listRunning = []
    listFaliur = []
    listPending = []
    listSuccess = []
    listRetry = []
    listStarted = []
    for el in tList:
        if el.pip_id.owner == request.user:
            status = settings.APP.AsyncResult(el.task_id).status
        if (status == 'PENDING'):
            listPending.append(el)
        if (status == 'STARTED'):
            listStarted.append(el)
        if (status == 'RETRY'):
            listRetry.append(el)
        if (status == 'SUCCESS'):
            listSuccess.append(el)
        if (status == 'RUNNING'):
            listRunning.append(el)
        else:
            listFaliur.append(el)
    context = {
    'listPending': listPending,
    'listStarted': listStarted,
    'listRetry': listRetry,
    'listSuccess': listSuccess,
    'listRunning': listRunning,
    'listFaliur': listFaliur,

    }
    return render(request, 'preprocess/status.html', context)
