__author__ = 'filippo'
from django import forms


class NUploadFileForm(forms.Form):
    fileData = forms.FileField()
    fileLabel = forms.FileField()
    fileSamples = forms.FileField()
    fileFeature = forms.FileField()
    fileRank = forms.FileField()
    fileMetrics = forms.FileField()

class files():
    def __init__(self, fileData, fileLabel, fileSamples, fileFeature, fileRank, fileMetrics):
        self.fileData = fileData
        self.fileLabel = fileLabel
        self.fileSamples = fileSamples
        self.fileFeature = fileFeature
        self.fileRank = fileRank
        self.fileMetrics = fileMetrics