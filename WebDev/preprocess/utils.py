from django.conf import settings
import os
import datetime
__author__ = 'filippo'
def handle_uploaded_file(f):
    #upload_dir = datetime.date.today().strftime(settings.UPLOAD_PATH)
    #upload_full_path = os.path.join(settings.MEDIA_PREPROCESS_ROOT, upload_dir)
    upload_full_path = settings.MEDIA_PREPROCESS_ROOT
    if not os.path.exists(upload_full_path):
        os.makedirs(upload_full_path)

    with open(os.path.join(upload_full_path, f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)