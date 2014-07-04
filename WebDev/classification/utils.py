from django.conf import settings
import os
import datetime
__author__ = 'filippo'
def handle_uploaded_file(user, pk, f):

    #upload_dir = datetime.date.today().strftime(settings.UPLOAD_PATH)
    #upload_full_path = os.path.join(settings.MEDIA_CLASSIFICATION_ROOT, upload_dir)
    upload_full_path = os.path.join(settings.MEDIA_CLASSIFICATION_ROOT,user)
    upload_full_path = os.path.join(upload_full_path,str(pk))

    if not os.path.exists(upload_full_path):
        os.makedirs(upload_full_path)

    with open(os.path.join(upload_full_path, f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)