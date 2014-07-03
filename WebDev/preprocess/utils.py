from django.conf import settings
import os


__author__ = 'filippo'
def handle_uploaded_file(f):

    upload_dir = date.today().strftime(settings.UPLOAD_PATH)
    upload_full_path = os.path.join(settings.MEDIA_ROOT, upload_dir)

    if not os.path.exists(upload_full_path):
        os.makedirs(upload_full_path)

    with open(upload_full_path+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)