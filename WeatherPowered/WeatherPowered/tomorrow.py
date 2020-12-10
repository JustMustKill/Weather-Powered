from django.shortcuts import render
import requests
from datetime import datetime
import datetime as DT


def sumOfList(numList):
    if len(numList) == 1:
        return numList[0]
    else:
        return numList[0] + sumOfList(numList[1:])


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

    hour = []
    averageTemp = []
    averagePressure = []
    averageHumidity = []
    averageWind_speed = []
    averageWind_deg = []
    arrayOfIcon = []
    i = 0
    offset = data_1['timezone_offset']

    now = data_1['hourly'][i]['dt'] + offset
    clear_2 = datetime.utcfromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
    clear_3 = datetime.utcfromtimestamp(now).strftime('%Y-%m-%d')
    dt = DT.datetime.fromisoformat(str(clear_3) + ' 03:00:00')
    clear = datetime.utcfromtimestamp(dt.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
    unix = (dt.timestamp() + 86400 - now) / 3600

    x = i + int(unix) + int(offset / 3600)
    max_value = 0

    date_buf = data_1['hourly'][x]['dt']
    date = datetime.utcfromtimestamp(date_buf).strftime('%d.%m.%Y')

    while x <= 47:
        if max_value != 8:
            ts = data_1['hourly'][x]['dt']
            buf_sunrise = data_1['current']['sunrise'] + offset
            buf_sunset = data_1['current']['sunset'] + offset
            buf_lengthOfDay = buf_sunset - buf_sunrise
            sunset = datetime.utcfromtimestamp(buf_sunset).strftime('%H:%M')
            sunrise = datetime.utcfromtimestamp(buf_sunrise).strftime('%H:%M')
            lengthOfDayHour = str(datetime.utcfromtimestamp(buf_lengthOfDay).strftime('%H'))
            lengthOfDayMinute = str(datetime.utcfromtimestamp(buf_lengthOfDay).strftime('%M'))
            lengthOfDay = lengthOfDayHour + 'ч ' + lengthOfDayMinute + 'мин'
            hour.append(datetime.utcfromtimestamp(ts).strftime('%H'))
            averageTemp.append(data_1['hourly'][x]['temp'])
            averagePressure.append(round(data_1['hourly'][x]['pressure'] * 0.00750062 * 100))
            averageHumidity.append(data_1['hourly'][x]['humidity'])
            averageWind_speed.append(data_1['hourly'][x]['wind_speed'])
            averageWind_deg.append(data_1['hourly'][x]['wind_deg'])
            buf = str(data_1['hourly'][x]['weather'][0]['icon'])
            if buf.endswith('n'):
                arrayOfIcon.append(buf.rstrip('n'))
            else:
                arrayOfIcon.append(buf.rstrip('d'))
            x = x + 3
        else:
            break

    tempOfTomorrow = round(sumOfList(averageTemp) / len(averageTemp), 1)
    pressureOfTomorrow = round(sumOfList(averagePressure) / len(averagePressure))
    humidityOfTomorrow = round(sumOfList(averageHumidity) / len(averageHumidity))
    windOfTomorrow = round(sumOfList(averageWind_speed) / len(averageWind_speed), 1)

    return render(request, 'tomorrow.html', {'location': nameCity,
                                             'temperature': tempOfTomorrow, 'wind': windOfTomorrow,
                                             'humidity': humidityOfTomorrow, 'pressure': pressureOfTomorrow,
                                             'icon': data['weather'][0]['icon'], 'hour': hour,
                                             'averageTemp': averageTemp, 'averageWind': averageWind_speed,
                                             'averageDeg': averageWind_deg, 'averagePressure': averagePressure,
                                             'averageHumidity': averageHumidity, 'sunset': sunset, 'sunrise': sunrise,
                                             'lengthOfDay': lengthOfDay, 'date': date, 'arrayOfIcon': arrayOfIcon})



def aboutUserInput(request):
    nameCity = request.GET['userInput']
    return about(request, nameCity)
