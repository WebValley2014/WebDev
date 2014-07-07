import datetime
from WebDev.models import *
from django.contrib.auth.decorators import login_required
import uuid
from forms import PPUploadFileForm
from django.shortcuts import render, HttpResponseRedirect
import djcelery
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from utils import pick_file_list
from django.shortcuts import  HttpResponse
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
def store_before_celery( pip_id ,jinput , task_id , tmpdir):
    '''

    This Function Stores the running process and info related to the results to the database.
    Needs to be called directly after [variable]= celery.start_task()

    :param pip_id: pipeline ID from Pipeline model.
    :param jinput: Dictionary of Inputs
    :param task_id: taskid
    :return: RunningProcess Database
    '''
    pname= 'Preprocessing'
    rundb = RunningProcess(
                         process_name=pname,
                         pip_id=pip_id,
                         inputs=jinput,
                         submitted = datetime.datetime.now() ,
                         task_id = taskid,
                         started = NULL,
                         finished = NULL ,
                     )

    return rundb

def store_after_celery(rundb , task_ret ):
    '''
    Run after Celery Task
    :param rundb: from store_before_celery
    :param task_ret:  return of the celery task
    :return: True
    '''

    tp = 'txt'
    rundb.started = task_ret.st,
    rundb.finished = task_ret.ft,

    resdb = Results(
                         process_name=rundb.process_name,
                         task_id = rundb.task_id,
                         filepath=task_ret.funct.pathname ,
                         filetype=tp,
                         filename=task_ret.funct.filename ,
                     )

    return True

