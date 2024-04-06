"""
URL configuration for wealthweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home'),
    path('portfolio/', views.portfolio_view, name='portfolio'),
    path('portfolio/currency-converter', views.convert_currency_view, name='currency-converter'),
    path('portfolio/reports', views.portfolio_reports_view, name='currency-converter'),
    path('about/', views.about_view, name='about'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('convert/', views.convert_currency_view, name='convert_currency'),

    path('admin/', admin.site.urls),
    path('btcusd/', views.get_bitcoin_price, name='btcusd'),
]
