import requests
import datetime  # для перевода секунд раcсвета и заката с 1 января 1970 в норм вид
import config
import pytz  # GMT+3
#from pprint import pprint  # что бы красиво разложить файл json


#from config import open_weather_token

def get_weather(name):
    smile = {
        "Clear": "\U00002600",  # Ясно
        "Clouds": "\U00002601",  # Облачно
        "Rain": "\U00002614",  # Дождь
        "Drizzle": "\U00002614",  # Дождь
        "Thunderstorm": "\U000026A1",  #Гроза
        "Snow": "\U00002744",  # Снег
        "Mist": "\U00001F32B"  # Туман
    }

    try:
        r2 = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={name}&appid={config.open_weather_token}&lang={'ru'}&units=metric")
        data2 = r2.json()
        #print('****')
        #pprint(data2)
        city = data2['name']
        temp = data2['main']['temp']
        feels_like = data2['main']['feels_like']
        humidity = data2['main']['humidity']
        pressure = data2['main']['pressure']
        weather = data2['weather'][0]['description']  # состояние облачно, ясно и т.д
        weather_description = data2['weather'][0]['main']
        weather_smile = smile[weather_description]
        wind = data2['wind']['speed']
        sunrise = datetime.datetime.fromtimestamp(data2['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data2['sys']['sunset'])
        #length_day = str(datetime.datetime.fromtimestamp(data2['sys']['sunset'] - data2['sys']['sunrise']))

        old_timezone = pytz.timezone("GMT")
        new_timezone = pytz.timezone("Europe/Moscow")
        sunrise_gmt3 = old_timezone.localize(sunrise).astimezone(new_timezone)
        snrsgmt3 = (str(sunrise_gmt3).split()[1]).split('+')[0]
        sunset_gmt3 = old_timezone.localize(sunset).astimezone(new_timezone)
        sstgmt3 = (str(sunset_gmt3).split()[1]).split('+')[0]
        length_day = str(sunset_gmt3 - sunrise_gmt3)


        s = (f'Погода в городе: {city} \nТемпература: {round(temp,1)}С° {weather} {weather_smile} \n'
              f'Ощущается как: {round(feels_like, 1)}С° \nВлажность: {humidity}% \nДавление: {pressure}мм.рт.ст \n'
              f'Ветер: {wind} м/с \nВосход солнца (GMT+3): {snrsgmt3} \nЗаход солнца (GMT+3): {sstgmt3} \n'
             f'Продолжительность дня: {length_day}')
        #print(s)
        return (s)
    except Exception as ex:
        #print(ex)
        return("Проверьте название города")

def Coordinates(city_name):
    try:
        r = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={5}&appid={config.open_weather_token}")
        data = r.json()
        #pprint(data)
        return get_weather(data[0]["lat"], data[0]["lon"])
    except Exception as ex:
        return ("Проверьте название города")
        #print(ex)