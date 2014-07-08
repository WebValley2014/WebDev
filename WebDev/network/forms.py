__author__ = 'filippo'
from django import forms


class NUploadFileForm(forms.Form):
    fileData = forms.FileField()
    fileLabel = forms.FileField()
    fileSamples = forms.FileField()
    fileFeature = forms.FileField()
    fileRank = forms.FileField()