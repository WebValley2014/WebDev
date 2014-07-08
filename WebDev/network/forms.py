__author__ = 'filippo'
from django import forms


class NUploadFileForm(forms.Form):
    fileData = forms.FileField()
    fileLabel = forms.FileField()
    fileSamples = forms.FileField()
    fileFeature = forms.FileField()
    fileRank = forms.FileField()

class files():
    def __init__(self, fileData, fileLabel, fileSamples, fileFeature, fileRank):
        self.fileData = fileData
        self.fileLabel = fileLabel
        self.fileSamples = fileSamples
        self.fileFeature = fileFeature
        self.fileRank = fileRank