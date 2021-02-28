from django.shortcuts import render, redirect
from .forms import PaymentForm
from django.http import HttpResponse

# Create your views here.
def checkout(request):
	if request.method == 'POST':
		form = PaymentForm(request.POST)
		if form.is_valid:
			print('payment successful')
			context ={
				'form':form,
				'buttonText':"Pay",
				'action':"",
				'title':"Checkout"
			}
			return render(request, 'form.html',context)
	else:
		form = PaymentForm()
		context ={
			'form':form,
			'buttonText':"Pay",
			'action':"",
			'title':"Checkout"
		}
		return render(request, 'form.html',context)