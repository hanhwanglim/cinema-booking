from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login

from .models import User
from .forms import LoginForm


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            return redirect('index')

        else:
            return redirect('login')
    else:
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, 'users/login.html', context)