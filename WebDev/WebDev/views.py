from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Template, Context
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
#import django.contrib.auth.views.login


def index(request):
    template = loader.get_template('index.html')
    context = Context({'user': request.user})
    return HttpResponse(template.render(context))

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url="/login")
def upload(request):
    return HttpResponse("UPLOAD")
