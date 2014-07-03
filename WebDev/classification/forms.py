__author__ = 'filippo'
from django import forms


class CLUploadFileForm(forms.Form):
    file = forms.FileField()