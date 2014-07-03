__author__ = 'filippo'
from django import forms


class CLUploadFileForm(forms.Form):
    file1 = forms.FileField()
    file2 = forms.FileField()
    file3 = forms.FileField()