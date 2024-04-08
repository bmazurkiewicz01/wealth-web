from django.db import models
from django.conf import settings
from django.utils import timezone

CURRENCY_SYMBOLS = {
    'USD': '$',
    'PLN': 'zł',
    'EUR': '€',
    'JPY': '¥',
}

class Investment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    trade_date = models.DateField(default=timezone.now)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='PLN')
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    exchange_rate = models.DecimalField(max_digits=20, decimal_places=15)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def currency_symbol(self):
        return CURRENCY_SYMBOLS.get(self.currency, '')