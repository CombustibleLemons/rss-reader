# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
import logging

def index(request):
	template = "index.html"
	return render(request, template, {})

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