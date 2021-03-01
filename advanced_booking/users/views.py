from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.contrib.auth import views

from .models import User
from payment.models import Order
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            # FIXME the form always returns the error message password_mismatch
            # despite the problem of the user entering an existing email or username
            context = {
                'form': RegisterForm(),
                'error_message': form.error_messages
            }
            return render(request, 'users/register.html', context)
    else:
        form = RegisterForm()
        context = {
            'form': form
        }
        return render(request, 'users/register.html', context)


def booking(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_order = Order.objects.filter(user=current_user)
        context = {
            'user': current_user,
            'order': user_order
        }
        return render(request, 'users/booking.html', context)
    return redirect(reverse('login'))
