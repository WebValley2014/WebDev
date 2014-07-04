from django.shortcuts import render, HttpResponseRedirect
import djcelery
from .tasks import add
from WebDev.models import *

from django.contrib.auth.decorators import login_required
from django.shortcuts import  HttpResponse
# Create your views here.

from forms import PPUploadFileForm
from utils import handle_uploaded_file

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


