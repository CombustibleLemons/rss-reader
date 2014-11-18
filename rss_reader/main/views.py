# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
import logging

def index(request):
	template = "index.html"
	return render(request, template, {})

def login(request):
	template = "login.html"
	return render(request, template, {"form":AuthenticationForm})