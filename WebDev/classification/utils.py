from django.conf import settings
from django.shortcuts import HttpResponse
import os
from django.core.servers.basehttp import FileWrapper
import mimetypes
from WebDev.models import *

__author__ = 'filippo'
def handle_uploaded_file(user, pk, f):

    #upload_dir = datetime.date.today().strftime(settings.UPLOAD_PATH)
    #upload_full_path = os.path.join(settings.MEDIA_CLASSIFICATION_ROOT, upload_dir)
    upload_full_path = os.path.join(settings.MEDIA_CLASSIFICATION_ROOT,user)
    upload_full_path = os.path.join(upload_full_path,str(pk))

    if not os.path.exists(upload_full_path):
        os.makedirs(upload_full_path)

    with open(os.path.join(upload_full_path, 'file'), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

#This function generate the response to download the file that is linked in file_path
def download_file(filename, file_path):
    wrapper = FileWrapper(open(file_path))
    content_type = mimetypes.guess_type(file_path)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length'] = os.path.getsize(file_path)
    response['Content-Disposition'] = "attachment; filename=%s"%filename
    return response

#This function check if the user is the owner of the Pipeline
def check_owner(user, p_id):
    pip = Pipeline.objects.filter(id=int(p_id))[0]
    if pip.owner == user:
        return True
    else:
        return False