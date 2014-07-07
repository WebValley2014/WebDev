from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from WebDev.models import *
from django.utils import timezone
import uuid

# Create your views here.

from forms import NUploadFileForm
from WebDev.utils import *

@login_required(login_url="/login")
def network(request, p_id = ''):
    if(p_id == ''):
        return HttpResponseRedirect('upload')
    return HttpResponse(p_id)

@login_required(login_url="/login")
def upload_network(request):
    form = NUploadFileForm()
    if not form.is_valid() and request.POST:
        messages.warning(request, 'No uploaded file')
    if request.POST and request.FILES:
        if checkExtension(request.FILES['file'], 'codes'):
            form = NUploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                p = Pipeline(pip_name='network', pip_id=str(uuid.uuid1()), started=timezone.now(), description='', owner=request.user)
                p.save()
                handle_uploaded_file(p,request.FILES['file'])
                return render(request, 'network/tuttook.html')
        else:
            messages.error(request, 'Wrong file type')
    return render(request, 'network/network.html')
