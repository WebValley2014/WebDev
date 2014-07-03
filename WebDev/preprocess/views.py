from django.shortcuts import render

# Create your views here.
def preprocess(request):
    return render(request, 'preprocess/preprocess.html')