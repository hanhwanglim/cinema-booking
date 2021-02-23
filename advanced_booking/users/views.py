from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login

from .models import User
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
        context = {
            'form': form
        }
        return render(request, 'users/register.html', context)