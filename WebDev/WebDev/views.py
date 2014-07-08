from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def about_us(request):
    return render(request, 'about_us.html')

# FARINA

def graph_prova(request):
    return render(request, 'graph_prova.html')

def graph_prova_oculus(request):
    return render(request, 'graph_prova_oculus.html')

# STEFANO

def graph_2d(request):
    return render(request, 'graph_2d.html')
