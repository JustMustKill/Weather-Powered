from django.shortcuts import render
from django.template import RequestContext
import requests
import json


def about(request):
    send_url = "http://api.ipstack.com/check?access_key=cd7895b611495437d7aa9632c46088f1&format=1&language=ru"
    geo_req = requests.get(send_url)
    geo_json = json.loads(geo_req.text)
    city = geo_json['city']
    country = geo_json['country_name']
    location = city + ", " + country

    res = requests.get("http://api.openweathermap.org/data/2.5/weather?appid=69d5ad0b3ba2922ca362149d36b229a0",
                       params={'q': location, 'units': 'metric', 'lang': 'RU'})
    data = res.json()
    return render(request, 'home.html', {'location': location, 'weather': data['weather'][0]['description'],
                                         'temperature': data['main']['temp'], 'wind': data['wind']['speed'],
                                         'humidity': data['main']['humidity'],
                                         'pressure': round(data['main']['pressure'] * 0.00750062 * 100),
                                         'icon': data['weather'][0]['icon']})


def handler404(request, *args, **argv):
    response = render('404.html', {})
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render('500.html', {})
    response.status_code = 500
    return response
