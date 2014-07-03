__author__ = 'filippo'
from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file1 = forms.FileField()
    file2 = forms.FileField()
    file3 = forms.FileField()