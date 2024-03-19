from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class CurrencyConversionForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2, max_digits=12, label='Amount')
    from_currency = forms.CharField(max_length=3, label='From Currency (e.g., USD)')
    to_currency = forms.CharField(max_length=3, label='To Currency (e.g., PLN)')
