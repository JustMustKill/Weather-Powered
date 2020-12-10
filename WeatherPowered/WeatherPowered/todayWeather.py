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
                         params={'lat': coord_lat, 'lon': coord_lon, 'exclude': 'daily,minutely', 'units': 'metric',
                                 'lang': 'RU'})
    data_1 = res_1.json()

    offset = data_1['timezone_offset']
    i = 0
    now_buf = data_1['hourly'][i]['dt'] + offset
    now = datetime.utcfromtimestamp(now_buf).strftime('%d.%m.%Y %H:%M:%S')
    now_date = datetime.utcfromtimestamp(now_buf).strftime('%d.%m.%Y')
    now_clock = datetime.utcfromtimestamp(now_buf).strftime('%H:%M')

    clear_3 = datetime.utcfromtimestamp(now_buf).strftime('%Y-%m-%d')
    dt = DT.datetime.fromisoformat(str(clear_3) + ' 03:00:00')
    clear = datetime.utcfromtimestamp(dt.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
    unix = (dt.timestamp() + 86400 - now_buf) / 3600
    x = i + int(unix) + int(offset / 3600)

    next_buf = data_1['hourly'][x]['dt']
    next = datetime.utcfromtimestamp(next_buf).strftime('%d.%m.%Y')

    hour = []
    averageTemp = []
    averagePressure = []
    averageHumidity = []
    averageWind_speed = []
    averageWind_deg = []
    arrayOfIcon = []

    while i < 22:
        offset = data_1['timezone_offset']
        buf_sunrise = data_1['current']['sunrise'] + offset
        buf_sunset = data_1['current']['sunset'] + offset
        buf_lengthOfDay = buf_sunset - buf_sunrise
        sunset = datetime.utcfromtimestamp(buf_sunset).strftime('%H:%M')
        sunrise = datetime.utcfromtimestamp(buf_sunrise).strftime('%H:%M')
        lengthOfDayHour = str(datetime.utcfromtimestamp(buf_lengthOfDay).strftime('%H'))
        lengthOfDayMinute = str(datetime.utcfromtimestamp(buf_lengthOfDay).strftime('%M'))
        lengthOfDay = lengthOfDayHour + 'ч ' + lengthOfDayMinute + 'мин'
        ts = data_1['hourly'][i]['dt'] + offset
        hour.append(datetime.utcfromtimestamp(ts).strftime('%H'))
        averageTemp.append(data_1['hourly'][i]['temp'])
        averagePressure.append(round(data_1['hourly'][i]['pressure'] * 0.00750062 * 100))
        averageHumidity.append(data_1['hourly'][i]['humidity'])
        averageWind_speed.append(data_1['hourly'][i]['wind_speed'])
        averageWind_deg.append(data_1['hourly'][i]['wind_deg'])
        buf = str(data_1['hourly'][i]['weather'][0]['icon'])
        if buf.endswith('n'):
            arrayOfIcon.append(buf.rstrip('n'))
        else:
            arrayOfIcon.append(buf.rstrip('d'))
        i = i + 3

    return render(request, 'today.html', {'location': nameCity, 'weather': data['weather'][0]['description'],
                                          'temperature': data['main']['temp'], 'wind': data['wind']['speed'],
                                          'humidity': data['main']['humidity'], 'pressure': round(data['main']['pressure'] * 0.00750062 * 100),
                                          'icon': data['weather'][0]['icon'], 'hour': hour, 'averageTemp': averageTemp, 'averageWind': averageWind_speed,
                                          'averageDeg': averageWind_deg,'averagePressure': averagePressure,
                                          'averageHumidity': averageHumidity, 'sunset': sunset, 'sunrise': sunrise,
                                          'now_date': now_date, 'now_clock': now_clock, 'next': next,
                                          'lengthOfDay': lengthOfDay, 'arrayOfIcon': arrayOfIcon})

def aboutUserInput(request):
    nameCity = request.GET['userInput']
    return about(request, nameCity)