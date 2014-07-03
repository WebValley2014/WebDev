__author__ = 'filippo'
def handle_uploaded_file(f):
    with open('classification/uploadedFiles/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)