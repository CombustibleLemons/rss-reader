# Create your views here.
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import UserForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
import logging

@login_required(login_url="/account/login/")
def index(request):
    template = "index.html"
    return render(request, template, {})

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # print "HELLO!"
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render_to_response(
            'registration/register.html',
            {'user_form': user_form, 'registered': registered},
            context)

def login_user(request):
	state = "Please log in below..."
	username = password = ''
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

	return render_to_response('login.html', {'state':state, 'username': username, 'form':AuthenticationForm})
	#template = "login.html"
	#return render(request, template, {"form":AuthenticationForm})

def register(request):
	template = "register.html"
	return render(request, template, {"form":UserCreationForm})

def about(request):
	template = "about.html"
	return render(request, template, {})

def settings(request):
	template = "settings.html" 
	return render(request, template, {})

def search(request):
	template = "search.html"
	return render(request, template, {})

def profile(request):
    return HttpResponseRedirect("/")