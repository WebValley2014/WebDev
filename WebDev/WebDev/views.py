from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def about_us(request):
    return render(request, 'about_us.html')

# FARINA

def graph_3D(request):
    return render(request, '2Dgraph.html')

def graph_oculus_3D(request):
    return render(request, '3Dgraph_oculus.html')

def tree_graph(request):
	return render(request, 'tree_graph.html')

# STEFANO

def graph_2d(request):
    return render(request, '2Dgraph.html')
