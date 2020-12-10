from django.shortcuts import render
import requests
from datetime import datetime
import datetime as DT


def about(request, nameCity):
    res = requests.get("http://api.openweathermap.org/data/2.5/weather?appid=69d5ad0b3ba2922ca362149d36b229a0",
                       params={'q': nameCity, 'units': 'metric', 'lang': 'RU'})
    data = res.json()

    coord_lon = data['coord']['lon']
    coord_lat = data['coord']['lat']

    res_1 = requests.get("https://api.openweathermap.org/data/2.5/onecall?appid=69d5ad0b3ba2922ca362149d36b229a0",
                         params={'lat': coord_lat, 'lon': coord_lon, 'exclude': 'hourly,minutely', 'units': 'metric',
                                 'lang': 'RU'})
    data_1 = res_1.json()

    res_2 = requests.get("https://api.openweathermap.org/data/2.5/onecall?appid=69d5ad0b3ba2922ca362149d36b229a0",
                         params={'lat': coord_lat, 'lon': coord_lon, 'exclude': 'daily,minutely', 'units': 'metric',
                                 'lang': 'RU'})
    data_2 = res_2.json()

    offset = data_2['timezone_offset']
    i = 0
    now_buf = data_2['hourly'][i]['dt'] + offset
    now = datetime.utcfromtimestamp(now_buf).strftime('%d.%m.%Y %H:%M:%S')
    now_date = datetime.utcfromtimestamp(now_buf).strftime('%d.%m.%Y')
    now_clock = datetime.utcfromtimestamp(now_buf).strftime('%H:%M')

    clear_3 = datetime.utcfromtimestamp(now_buf).strftime('%Y-%m-%d')
    dt = DT.datetime.fromisoformat(str(clear_3) + ' 03:00:00')
    clear = datetime.utcfromtimestamp(dt.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
    unix = (dt.timestamp() + 86400 - now_buf) / 3600
    x = i + int(unix) + int(offset / 3600)

    next_buf = data_2['hourly'][x]['dt']
    next = datetime.utcfromtimestamp(next_buf).strftime('%d.%m.%Y')

    day = []
    month = []
    averageTemp = []
    averagePressure = []
    averageHumidity = []
    averageWind_speed = []
    averageWind_deg = []
    arrayOfIcon = []
    for i in range(8):
        offset = data_1['timezone_offset']
        ts = data_1['daily'][i]['dt']
        day.append(datetime.utcfromtimestamp(ts).strftime('%d'))
        month.append(datetime.utcfromtimestamp(ts).strftime('%m'))
        averageTemp.append(data_1['daily'][i]['temp']['eve'])
        averagePressure.append(round(data_1['daily'][i]['pressure'] * 0.00750062 * 100))
        averageHumidity.append(data_1['daily'][i]['humidity'])
        averageWind_speed.append(data_1['daily'][i]['wind_speed'])
        averageWind_deg.append(data_1['daily'][i]['wind_deg'])
        buf = str(data_1['daily'][i]['weather'][0]['icon'])
        arrayOfIcon.append(buf.rstrip('d'))

    return render(request, 'sevenDays.html', {'location': nameCity, 'weather': data['weather'][0]['description'],
                                              'temperature': data['main']['temp'], 'wind': data['wind']['speed'],
                                              'humidity': data['main']['humidity'],
                                              'pressure': round(data['main']['pressure'] * 0.00750062 * 100),
                                              'icon': data['weather'][0]['icon'], 'averageTemp': averageTemp,
                                              'day': day,
                                              'month': month, 'averageWind': averageWind_speed,
                                              'averageDeg': averageWind_deg,
                                              'averagePressure': averagePressure, 'averageHumidity': averageHumidity,
                                              'now_date': now_date, 'now_clock': now_clock,
                                              'next': next, 'arrayOfIcon': arrayOfIcon})


def aboutUserInput(request):
    nameCity = request.GET['userInput']
    return about(request, nameCity)
