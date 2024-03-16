from django import forms

class CurrencyConversionForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2, max_digits=12, label='Amount')
    from_currency = forms.CharField(max_length=3, label='From Currency (e.g., USD)')
    to_currency = forms.CharField(max_length=3, label='To Currency (e.g., PLN)')
