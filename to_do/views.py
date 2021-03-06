from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import ToDo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'signup.html',
                              {'form': UserCreationForm(), 'error': 'That username has already been taken. Please choose a new username'})

        else:
            return render(request, 'signup.html', {'form': UserCreationForm(), 'error': 'Passwords did not match'})

def loginuser(request):
		if request.method == 'GET':
				return render(request, 'login.html', {'form': AuthenticationForm()})
		else:
				user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
				if user is None:
						return render(request, 'login.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
				else:
						login(request, user)
						return redirect('currenttodos')

@login_required
def logoutuser(request):
		if request.method == 'POST':
				logout(request)
				return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'createtodo.html', {'form': Todoform(), 'error': 'Incorrect data passed. Please try again!'})



