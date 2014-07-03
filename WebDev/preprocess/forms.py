__author__ = 'filippo'
from django import forms


class PPUploadFileForm(forms.Form):
    file = forms.FileField()