from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.http import HttpResponseRedirect

from .forms import UserCreationForm
# Create your views here.

def login_view(request):
    '''
    Login View
    '''
    if not request.user.is_authenticated():
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = authenticate(email=request.POST['username'], password=request.POST['password'])
                if user is not None:
                    auth_login(request, user)
                    messages.add_message(request, messages.INFO, "toastr.success('"+user.username+"','Welcome back!');")
                    return HttpResponseRedirect('/index/')
        else:
            form = AuthenticationForm()
        return render(request, 'auth/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/index/')


def logout_view(request):
    '''
    Log the user out
    '''
    auth_logout(request)
    return HttpResponseRedirect('/')


def reg_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)     # create form object
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/index/')
    else:
        form = UserCreationForm()

    return render(request, 'auth/register.html', {'form': form})
