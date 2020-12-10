"""WeatherPowered URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from WeatherPowered import homePage
from WeatherPowered import todayWeather
from WeatherPowered import sevenDaysWeather
from WeatherPowered import tomorrow

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homePage.about),
    path('searchToday/', todayWeather.aboutUserInput, name='cityToday'),
    path('search/<str:nameCity>', todayWeather.about, name='city'),
    path('searchByCity/', sevenDaysWeather.aboutUserInput, name='citySevenDays'),
    path('search/sevenDays/<str:nameCity>', sevenDaysWeather.about, name='citySeven'),
    path('searchTomorrowByCity/', tomorrow.aboutUserInput, name='cityTomorrowDay'),
    path('search/tommorowDay/<str:nameCity>', tomorrow.about, name='cityTomorrow'),
]
