import requests
import config

#Uses the OpenWeatherMap API to get weather information at the location provided by the car
WEATHER_KEY=config.openweathermapCONST['apikey']#'741365596cedfc98045a26775a2f947d'

#gets generic weather information of the area
def get_weather(lat=30.6123149, lon=-96.3434963):
    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(str(lat), str(lon), WEATHER_KEY)
    r = requests.get(url)
    return r.json()

#isolates the temperature from the list and returns it to the main file
def weather(lat=30.6123149, lon=-96.3434963):
    weather = get_weather(lat, lon)
    temperature = weather['main']['temp']
    temperature = temperature - 273.15
    return str(temperature)

#creative descriptions of how the weather feels
def temperature_description(temperature="25"):
    temp = float(temperature)
    if temp < -30:
        return ", perfect weather for penguins."
    elif temp < -15:
        return ", you might want stay inside."
    elif temp < 0:
        return ", you should wear a few layers."
    elif temp < 10:
        return ", sure is chilly."
    elif temp < 20:
        return ", sweater weather!"
    elif temp < 30:
        return ", the weather looks great!"
    elif temp < 40:
        return ", ice cream weather!"
    elif temp < 45:
        return " stay inside and stay hydrated."
    else:
        return ", the A/C bill is going to be high."
