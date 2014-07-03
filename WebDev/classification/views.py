from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import  HttpResponse
# Create your views here.

from forms import CLUploadFileForm
from utils import handle_uploaded_file

@login_required(login_url="/login")
def classification(request):
    form = CLUploadFileForm()
    if request.POST and request.FILES:
        form = CLUploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file1'])
            handle_uploaded_file(request.FILES['file2'])
            handle_uploaded_file(request.FILES['file3'])
            return render(request, 'classification/tuttook.html')
        else:
            return render(request, 'classification/classification.html')
    return render(request, 'classification/classification.html')
