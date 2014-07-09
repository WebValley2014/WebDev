from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from WebDev.models import *
from WebDev.store import *
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



'''
To Michele : If I am asleep when you review this , see FIX ME in each view and in store.py and Debug.
'''













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

def step2(request, pip_id):
    '''
    #FIX ME : Doesn't Handle the Arguments .
              HttpsResponseRedirect : Give the right URL.
    '''
    pip = Pipeline.objects.get(pip_id=pip_id)
    file_otu = Results.objects.get(pip_id=pip, process_name='processing', filetype='cl_otu')
    file_class = Results.objects.get(pip_id=pip, process_name='processing', filetype='cl_class')

    print 'Celery in launch'
    ml_id = settings.APP.send_task("ml", (pip.pip_id, file_otu.filepath, file_class.filepath))
    print
    print 'Celery launched'


    input_data = {'file_OTU': file_otu.filepath, 'file_CLASS': file_class.filepath}
    print  'Process Started'
    store_before_celery(pip, input_data, ml_id.id, "classification")
    print  'Saving Process to database'

    return HttpResponseRedirect("/class/processing/" + ml_id.id + "/")

def learning_loading (request, task_id):
    '''
    FIX ME : Correct the HTTP RESPONSE
    '''
    # Pick the results
    result = settings.APP.AsyncResult(task_id)
    print str(result.status)
    print str(settings.APP)
    if result.ready():
        return HttpResponseRedirect('/class/processing_finish/%s/' % (task_id,))
    else:
        return HttpResponse(result.status)

def learning_finish(request, task_id):
    '''
    FIX ME : Correct the HTTP RESPONSE
    '''
    # Pick the results
    result = settings.APP.AsyncResult(task_id)
    if result.ready():
        r = result.get()
        rp = RunningProcess.objects.get(task_id=task_id)
        if store_after_celery_class(rp, r, 'txt'):
            return HttpResponse('OK')
        else:
            return HttpResponse('Error')
    return HttpResponseRedirect('/preproc/processing/%s/' % (task_id,))


@login_required(login_url="/login")
def upload_preProcessed(request):
    form_error = False
    if request.POST:
        if request.FILES:
            print str(request.FILES)
            try:
                file_otu = request.FILES['file_otu']
                file_class = request.FILES['file_class']
            except:
                messages.error(request, "Insert the correct files")
                form_error = True

            if not form_error:
                li = [file_otu.name, file_class.name]
                if not different(li):
                    form_error = True
                    messages.error(request, "Some files with the same name")
            if not form_error:
                if checkExtension(file_otu, 'txt') and checkExtension(file_class, 'txt'):
                    p = Pipeline(pip_name='classification', pip_id=hashlib.md5(str(uuid.uuid1())).hexdigest(),
                                 started=timezone.now(), description='', owner=request.user)
                    p.save()

                    handle_uploaded_file(p,file_otu,"processing", 'cl_otu')
                    handle_uploaded_file(p,file_class,"processing", 'cl_class')
                    return HttpResponse('/class/step2/%s/' % (p.pip_id,))
                else:
                    messages.error(request, "File type incorrect")
        else:
            messages.error(request, "Insert the correct files")
        return HttpResponse('/class/upload/')
    oldFiles = Results.objects.filter(process_name='Preprocessing', owner=request.user)
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

    #Retrive the download
    return download_file("file.txt", download_path)

def option(request, p_id):
    return render(request, 'classification/option.html', {'p_id': p_id})