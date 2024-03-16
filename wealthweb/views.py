from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .forms import CurrencyConversionForm
import requests

def get_bitcoin_price(request):
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
    response = requests.get(url)
    
    data = response.json()
    
    btc_to_usd = data.get('bitcoin', {}).get('usd', 'Unavailable')
    
    return JsonResponse({'BTC to USD': btc_to_usd})

def convert_currency(request):
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
                # For simplicity, we'll render the result on the same page
                return render(request, 'conversion_result.html', {
                    'form': form,
                    'conversion_result': conversion_result,
                    'from_currency': from_currency,
                    'to_currency': to_currency
                })
            else:
                # Handle errors or invalid API response
                conversion_result = 'Error: Unable to fetch conversion rate'
    else:
        form = CurrencyConversionForm()  # Instantiate an empty form for GET requests
    
    # Render the initial form page
    return render(request, 'convert_currency.html', {'form': form})