# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
import logging

def index(request):
    template = "index.html"
    return render(request, template, {})

#from https://docs.djangoproject.com/en/dev/topics/auth/default/#auth-web-requests
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        #if user.is_active:
        login(request, user)
        return HttpResponseRedirect("a success page .html")
        #else:
            # Return a 'disabled account' error message
            # I'm not sure this is necessary in our case:
            ## "If you want to reject a login based on is_active, check that in your own login/custom authentication backend"
            ## from https://docs.djangoproject.com/en/1.7/ref/contrib/auth/
    else:
        # Return an 'invalid login' error message.
        # this shouldn't really error/exception, as much as just have a different outcome, right?
        return HttpResponse("Your Username or Password is invalid")

def logout_view(request):
    logout(request)
    # Redirect to a success page.

# using http://www.tangowithdjango.com/book/chapters/login.html
def register_view(request):
    #initially registered is false
    registered = False

    #make a userform
    user_form = UserForm(data=request.POST) #forms.py has a user_form, you can put data in it
    if user_form.is_valid():
        user = user_form.save()

        #set a password for the user
        user.set_password(user.password)
        user.save()

        registered = True

    else:
        print user_form.errors
