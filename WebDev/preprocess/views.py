from django.shortcuts import render, HttpResponseRedirect
import djcelery
from .tasks import add
from WebDev.models import *
from django.contrib.auth.decorators import login_required
import uuid
from django.utils import timezone
from utils import pick_file_list
from django.shortcuts import  HttpResponse
from forms import PPUploadFileForm
from WebDev.utils import *
from django.contrib import messages


@login_required(login_url="/login")
def preprocess_redirect(request):
    return HttpResponseRedirect("upload/")

@login_required(login_url="/login")
def get_results(request, p):
    return

@login_required(login_url="/login")
def upload(request):

    form_error, ex_error = False, False
    #IF FIELE UPLOADED
    if request.POST:
        if request.FILES:
            try:
                file_zip = request.FILES['file_zip']
                file_map = request.FILES['file_map']
            except:
                messages.error(request, "Insert the correct file")
            if not form_error:
                if checkExtension(file_zip, 'zip') and checkExtension(file_map, 'map'):
                    p = Pipeline(pip_name='preprocess', pip_id=str(uuid.uuid1()), started=timezone.now(), description='', owner=request.user)
                    p.save()
                    handle_uploaded_file(p, file_zip)
                    handle_uploaded_file(p, file_map)
                    return HttpResponseRedirect('/preproc/celery/'+p.pip_id)
                else:
                    messages.error(request, "File type incorrect")
        else:
            messages.error(request, "Insert the correct file")

    #ELSE GENERATE THE FILE UPLOAD PAGE
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
    re1 = Results.objects.get(id=int(id1))
    re2 = Results.objects.get(id=int(id2))
    delete(re1)
    delete(re2)
    return HttpResponseRedirect('/preproc/upload')

@login_required(login_url="/login")
def celery(request, pip_id, new_pip=0):
    return HttpResponse(new_pip)
    #pip = Pipeline.objects.get(pip_id=uuid)
    #file = Results.objects.filter(pip_id=pip, process_name='preprocess')
    #
    #
    #
    #
    #
    #return HttpResponseRedirect('/preproc/processing/process_name/')

@login_required(login_url='/login')
def processing(request, process_name):
    # PROCESSING
    # OR
    # FINISHED
    return HttpResponse("PROCESSING")













#Da eliminare


@login_required(login_url="/login")
def preprocess(request):

    form = PPUploadFileForm()
    if request.POST and request.FILES:
        form = PPUploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('launch')

    return render(request, 'preprocess/preprocess.html')

def submit_celery(request):

    t = add.delay(4,4)

    # runp = RunningProcess(process_name='Preprocessing',
    #                     task_id=t.id,
    #                     pip_id = Pipeline.objects.get(pip_id=uuid))
    context = {'uuid': t.id}

    return render(request, 'preprocess/proc_res.html', context)

def get_results(request, uuid):

    task =  djcelery.celery.AsyncResult(uuid)
    context = {'task': task}

    return render(request, 'preprocess/results.html', context)


