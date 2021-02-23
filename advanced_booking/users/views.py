from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.urls.base import reverse

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
        form = RegisterForm()
        context = {
            'form': form
        }
        return render(request, 'users/register.html', context)

    
def booking(request):
    if request.user.is_authenticated:
        current_user = request.user
        # print(Order.objects.get(user=1))  
        user_order = Order.objects.filter(user=current_user)
        print(user_order)
        context = {
            'user': current_user,
            'order': user_order
        }
        return render(request, 'users/booking.html', context)
    return redirect(reverse('login'))
    