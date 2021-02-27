#pip install django-credit-cards needed !!!!!!
from django import forms
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField

class PaymentForm(forms.Form):
    number = CardNumberField(label='Card Number')
    expiryDate = CardExpiryField(label='Expiration Date')
    securityCode = SecurityCodeField(label='CVV/CVC')
    name=forms.CharField(label="Name",error_messages={'required': 'Please enter the name written on your card.'})

