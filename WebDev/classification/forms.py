__author__ = 'filippo'
from django import forms


class CLUploadFileForm(forms.Form):
    file1 = forms.FileField()
    file2 = forms.FileField()

class files():
    def __init__(self, fileData, fileLabel, pip_id):
        self.file_otu = fileData
        self.file_class = fileLabel
        self.pip_id = pip_id