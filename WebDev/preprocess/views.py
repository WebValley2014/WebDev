from django.shortcuts import render, HttpResponseRedirect
import djcelery
from .tasks import add
from WebDev.models import *
from django.contrib.auth.decorators import login_required
import uuid
from django.utils import timezone
from django.shortcuts import  HttpResponse

from forms import PPUploadFileForm
from WebDev.utils import handle_uploaded_file, checkExtension, renameFile

@login_required(login_url="/login")
def preprocess_redirect(request):
    return HttpResponseRedirect("upload/")

@login_required(login_url="/login")
def get_results(request, p):
    return

@login_required(login_url="/login")
def upload(request):
    p = Pipeline(pip_name='preprocess', pip_id=str(uuid.uuid1()), started=timezone.now(), description='', owner=request.user)
    p.save()
    form_error, ex_error = False, False
    if request.POST:
        if request.FILES:
            try:
                file_zip = request.FILES['file_zip']
                file_map = request.FILES['file_map']
            except:
                form_error = True
            if not form_error:
                if checkExtension(file_zip, 'zip') and checkExtension(file_map, 'map'):
                    file_zip = renameFile(file_zip, 'archivio_zip')
                    file_map = renameFile(file_map, 'file_map')
                    handle_uploaded_file(p, file_zip)
                    handle_uploaded_file(p, file_map)
                    return HttpResponseRedirect('/preproc/celery/'+p.pip_id)
                else:
                    ex_error = True
        else:
            form_error = True
    form = PPUploadFileForm()
    c = {
        'ex_error': ex_error,
        'form_error': form_error
    }
    return render(request, 'preprocess/upload.html', c)

@login_required(login_url="/login")
def celery(request, uuid):
    pip = Pipeline.objects.get(pip_id=uuid)
    file = Results.objects.filter(pip_id=pip, process_name='preprocess')
    #
    #
    #
    #
    #
    return HttpResponseRedirect('/preroc/processing/process_name/')

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


