from django.conf import settings
from django.shortcuts import HttpResponse
import os
from django.core.servers.basehttp import FileWrapper
import mimetypes
from .models import *

# Returns the file extension
def fileExtension(f):
    u = f.name.split('.')
    return u[len(u)-1]

# Checks whether the file extension is equal to the given extension
def checkExtension(f,extension):
    return (fileExtension(f)==extension)

# Renames the file
def renameFile(f, filename):
    ex = fileExtension(f)
    f.name = '%s.%s' % (filename, ex)
    return f

# Saves the file in MEDIA_ROOT/username/uuid/app/file + stores the attributes of the file in the db
def handle_uploaded_file(pipeline, f, procName, filetype=None):
    if filetype==None:
        filetype = fileExtension(f)
    partial_path = os.path.join(pipeline.owner.username, str(pipeline.pip_id))
    partial_path = os.path.join(partial_path, procName)
    full_path = os.path.join(settings.MEDIA_ROOT, partial_path)
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    full_path=os.path.join(full_path, f.name)

    with open(full_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    res = Results(process_name=procName, owner=pipeline.owner , pip_id=pipeline, filetype=filetype, filename=f.name, filepath=full_path)
    res.save()

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

# Checkes wether the elements of a list are all different
def different(l):
    for i in range(len(l)):
        for j in range(i+1, len(l)):
            if(l[i]==l[j]):
                    return False
    return True

# Deletes the file corresponding to the given Results object
def delete(re):
    pos = re.filepath #pos = '.../utente/uuid/app/file'
    os.remove(pos)
    pos = os.sep.join(pos.split(os.sep)[:-1]) # pos = '.../utente/uuid/app'
    try:
        os.rmdir(pos)
        pos = os.sep.join(pos.split(os.sep)[:-1]) # pos = '.../utente/app'
        try:
            os.rmdir(pos)
        except:
            pass
    except:
        pass
    re.delete()

def swap(lis, a, b):
    t = lis[a]
    lis[a]=lis[b]
    lis[b] = t

def rotate(lis):
    for i in range(len(lis)/2):
        swap(lis, i, len(lis)-1-i)