# Create your views here.
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import UserForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response
import logging

@login_required(login_url="/accounts/login/")
def index(request):
    template = "index.html"
    return render(request, template, {"authenticated":True})

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
        # A boolean value for telling the template whether the registration was successful.
        # Set to False initially. Code changes value to True when registration succeeds.
        registered = False

        # If it's a HTTP POST, we're interested in processing form data.
        if request.method == 'POST':
            # Attempt to grab information from the raw form information.
            # Note that we make use of both UserForm.
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
                return HttpResponseRedirect("/")

            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            # They'll also be shown to the user.
            else:
                # NOTE: If we resend the response with the SAME form then it will send back errors
                # with the form.
                return render_to_response(
                        'registration/register.html',
                        {'user_form': user_form, 'registered': registered},
                        context)

        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        else:
            user_form = UserForm()
            # Render the template depending on txhe context.
            return render_to_response(
                    'registration/register.html',
                    {'user_form': user_form, 'registered': registered},
                    context)

def user_login(request):
    context = RequestContext(request)

    authenticated = request.user.is_authenticated()

    if authenticated:
        return HttpResponseRedirect("/")

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        #import pdb; pdb.set_trace()
        #print username
        #print password
        user = authenticate(username=username, password=password)
        #print user

        if user is not None:
            login(request, user)
            #print "logged in"
            return HttpResponseRedirect("/")
        else:
        #    print "user is None"
            return render_to_response('registration/login.html',
            {'form': AuthenticationForm(request.POST), "authenticated":authenticated},
                context)
    else:
        return render(request, 'registration/login.html', {'form': AuthenticationForm(), "authenticated": authenticated})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login")


def change_password(request):
    import pdb; pdb.set_trace()
    abc =34
    # if request.user.is_authenticated():

        # # If it's a HTTP POST, we're interested in processing form data.
        # if request.method == 'POST':
        #     u = User.objects.get(username=request.user.username)
        #     u.set_password('new password')
        #     u.save()
        # else:
        #     user_form = UserForm()
        #     # Render the template depending on txhe context.
        #     return render_to_response(
        #             'registration/register.html',
        #             {'user_form': user_form, 'registered': registered},
        #             context)    
