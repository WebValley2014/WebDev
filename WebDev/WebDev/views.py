from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Template, Context
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.shortcuts import render
from django.shortcuts import render_to_response
from forms import ContactForm, UploadFileForm


def index(request):
    template = loader.get_template('index.html')
    context = Context({'user': request.user})
    return HttpResponse(template.render(context))

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        # ContactForm was defined in the previous section
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            return HttpResponse(subject+"<br>"+message) # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render(request, 'contact.html', {
        'form': form,
    })

@login_required(login_url="/login")
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            name = f.name
            with open('WebDev/uploadedFiles/'+name, 'wb+') as destination:
                for chunk in f.chunks():
                     destination.write(chunk)
            return HttpResponse(name)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {
        'form': form,
        })