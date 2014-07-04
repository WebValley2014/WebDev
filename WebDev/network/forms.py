__author__ = 'filippo'
from django import forms


class NUploadFileForm(forms.Form):
    file = forms.FileField()