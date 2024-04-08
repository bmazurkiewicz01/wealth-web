from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import Investment
from .models import CURRENCY_SYMBOLS

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class InvestmentForm(forms.ModelForm):
    currency = forms.ChoiceField(choices=CURRENCY_SYMBOLS)
    class Meta:
        model = Investment
        fields = ['symbol', 'trade_date', 'quantity', 'currency', 'exchange_rate']
        widgets = {
            'trade_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'symbol': forms.TextInput(attrs={'placeholder': 'Enter Symbol, e.g., BTC'}),
            'quantity': forms.NumberInput(attrs={'step': 'any'}),
            'exchange_rate': forms.NumberInput(attrs={'step': 'any'}),
        }

CURRENCY_CHOICES = [
    ('USD', 'US Dollar'),
    ('EUR', 'Euro'),
    ('JPY', 'Japanese Yen'),
    ('PLN', 'Polish Zloty'),
]        
class CurrencyConversionForm(forms.Form):
    amount = forms.DecimalField(
        decimal_places=2, max_digits=12, label='Amount',
        widget=forms.NumberInput(attrs={'class': 'input amount-input', 'placeholder': 'Amount'})
    )
    from_currency = forms.ChoiceField(
        choices=CURRENCY_CHOICES, label='From',
        widget=forms.Select(attrs={'class': 'select from-currency-select'})
    )
    to_currency = forms.ChoiceField(
        choices=CURRENCY_CHOICES, label='To',
        widget=forms.Select(attrs={'class': 'select to-currency-select'})
    )

    def __init__(self, *args, **kwargs):
        super(CurrencyConversionForm, self).__init__(*args, **kwargs)
        self.fields['to_currency'].initial = 'PLN'
        self.fields['amount'].initial = '100'
