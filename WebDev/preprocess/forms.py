__author__ = 'filippo'
from django import forms

class PPUploadFileForm(forms.Form):
    file_sff = forms.FileField()
    file_map = forms.FileField()