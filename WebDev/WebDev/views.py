from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Template, Context
from django.contrib.auth import authenticate, login
#import django.contrib.auth.views.login


def index(request):
    template = loader.get_template('index.html')
    context = Context()
    return HttpResponse(template.render(context))

@login_required(login_url="/login")
def upload(request):
    return HttpResponse("UPLOAD")

