from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import CurrencyConversionForm
from .forms import UserRegistrationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
import requests


class LoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        else:
            return redirect(self.get_success_url())

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)
        else:
            return super().form_invalid(form)

def home_view(request):
    return render(request, 'home.html')

@login_required
def portfolio_view(request):
    return render(request, 'portfolio.html')

@login_required
def portfolio_reports_view(request):
    return render(request, 'portfolio_reports.html')

def about_view(request):
    return render(request, 'about.html')

def register_view(request):
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'register.html', context=context)

def convert_currency_view(request):
    if request.method == 'POST':
        form = CurrencyConversionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            from_currency = form.cleaned_data['from_currency'].upper()
            to_currency = form.cleaned_data['to_currency'].upper()
            
            api_key = settings.EXCHANGE_RATE_API_KEY
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}/{amount}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                conversion_result = data.get('conversion_result', 'Error fetching conversion rate')
                return render(request, 'convert_currency.html', {
                    'form': form,
                    'initial_amount': amount,
                    'converted_amount': conversion_result,
                    'from_currency': from_currency,
                    'to_currency': to_currency
                })
            else:
                conversion_result = 'Error: Unable to fetch conversion rate'
    else:
        form = CurrencyConversionForm() 
    return render(request, 'convert_currency.html', {'form': form})

def get_bitcoin_price(request):
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
    response = requests.get(url)
    
    data = response.json()
    
    btc_to_usd = data.get('bitcoin', {}).get('usd', 'Unavailable')
    
    return JsonResponse({'BTC to USD': btc_to_usd})
