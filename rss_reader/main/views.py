# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
import logging

def index(request):
	template = "index.html"
	return render(request, template, {})

def login(request):
	template = "login.html"
	return render(request, template, {"form":AuthenticationForm})

def register(request):
	template = "register.html"
	return render(request, template, {"form":UserCreationForm})

def about(request):
	template = "about.html"
	return render(request, template, {})