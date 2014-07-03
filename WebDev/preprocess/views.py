from django.shortcuts import render
import djcelery
from .tasks import add

# Create your views here.
def preprocess(request):
    return render(request, 'preprocess/preprocess.html')

def submit_celery(request):

    t = add.delay(4,4)

    context = {'uuid': t.id}
    return render(request, 'preprocess/proc_res.html', context)

def get_results(request, uuid):

    task =  djcelery.celery.AsyncResult(uuid)
    context = {'task': task}

    return render(request, 'preprocess/results.html', context)