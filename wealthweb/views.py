from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import CurrencyConversionForm
from .forms import UserRegistrationForm
from .forms import InvestmentForm
from .models import Investment
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from datetime import datetime
import requests
import matplotlib.pyplot as plt
import io
import urllib, base64


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
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            new_investment = form.save(commit=False)
            current_price = get_current_price(new_investment.symbol, new_investment.currency)
            new_investment.current_price = current_price if current_price else 0
            new_investment.user = request.user
            new_investment.save()
            return redirect('portfolio')
    else:
        form = InvestmentForm()

    investments = Investment.objects.filter(user=request.user)

    refresh_prices = bool(request.GET.get('refresh_prices', None))
    print("Refresh prices:", refresh_prices)

    for investment in investments:
        if refresh_prices:
            current_price = get_current_price(investment.symbol)
            print("Current price:", current_price)
            if current_price:
                investment.current_price = float(current_price)
                investment.save() 
        else:
            current_price = investment.current_price

        investment.current_price = float(current_price) * float(investment.quantity) if current_price else 0
        investment.total_value = (1 / investment.exchange_rate) * investment.quantity
        investment.return_value = float(investment.current_price) - float(investment.total_value)

    return render(request, 'portfolio.html', {
        'investments': investments,
        'form': form,
    })

def get_current_price(symbol, currency='USD'):
    if symbol:
        api_key = settings.STOCK_API_KEY
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
        response = requests.get(url)
        data = response.json()
        
        if 'Global Quote' in data:
            price = data['Global Quote']['05. price']
            if currency and currency != 'USD':
                api_key = settings.EXCHANGE_RATE_API_KEY
                url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/USD/{currency}/1"
                response = requests.get(url)
                data = response.json()
                price = float(price) * float(data.get('conversion_result', 1))

            return float(price) 
        else:
            return None  
    else:
        return None  

@require_POST
def portfolio_delete_view(request, investment_id):
    investment = get_object_or_404(Investment, pk=investment_id, user=request.user)
    investment.delete()
    return redirect('portfolio')  
    
@login_required
def get_exchange_rate_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)
    currency = request.GET.get('currency', None)

    if symbol and date:
        api_key = settings.STOCK_API_KEY
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={api_key}'
        response = requests.get(url)
        data = response.json()

        if 'Weekly Time Series' in data:
            weekly_data = data['Weekly Time Series']
            available_dates = list(weekly_data.keys())
            closest_date = min(available_dates, key=lambda x: abs(datetime.strptime(x, '%Y-%m-%d') - datetime.strptime(date, '%Y-%m-%d')))
            
            exchange_rate = weekly_data[closest_date]['4. close']
            if currency and currency != 'USD':
                print("Exchange rate in USD:", exchange_rate)
                api_key = settings.EXCHANGE_RATE_API_KEY
                url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/USD/{currency}/1"
                response = requests.get(url)
                data = response.json()
                exchange_rate = float(exchange_rate) * float(data.get('conversion_result', 1))
                print("Exchange rate in", currency, ":", exchange_rate)

            return JsonResponse({'exchangeRate': str(1 / float(exchange_rate)), 'date': closest_date})
        else:
            return JsonResponse({'error': 'Weekly time series data not found'}, status=404)
    else:
        return JsonResponse({'error': 'Symbol and date parameters are required'}, status=400)
    
@login_required
def get_stock_symbol_view(request):
    symbol = request.GET.get('symbol', None)
    if symbol:
        api_key = settings.STOCK_API_KEY  
        url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey={api_key}'
        response = requests.get(url)
        data = response.json()
        
        if 'bestMatches' in data:
            symbols = [item['1. symbol'] for item in data['bestMatches']]
            return JsonResponse({'symbols': symbols})
        else:
            return JsonResponse({'error': 'Symbols not found'}, status=404)
    else:
        return JsonResponse({'error': 'Symbol parameter is required'}, status=400)

def generate_investment_quantity_plot(investments):
    symbols = [investment.symbol for investment in investments]
    quantities = [investment.quantity for investment in investments]

    fig, ax = plt.subplots()
    ax.bar(symbols, quantities)
    ax.set_xlabel('Symbols')
    ax.set_ylabel('Quantities')
    ax.set_title('Investment Quantities per Symbol')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri

def generate_investment_return_plot(investments):
    symbols = [investment.symbol for investment in investments]
    return_values = [float(investment.current_price) - float((1 / investment.exchange_rate) * investment.quantity) for investment in investments]
    colors = ['red' if value < 0 else 'green' for value in return_values]

    fig, ax = plt.subplots()
    ax.bar(symbols, return_values, color=colors)
    ax.set_xlabel('Symbols')
    ax.set_ylabel('Return Value')
    ax.set_title('Return Value per Investment')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri

@login_required
def portfolio_reports_view(request):
    investments = Investment.objects.filter(user=request.user)
    quantity_plot = generate_investment_quantity_plot(investments)
    return_plot = generate_investment_return_plot(investments)
    return render(request, 'portfolio_reports.html', {'quantity_plot': quantity_plot, 'return_plot': return_plot})

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
