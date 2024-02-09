import requests
from config import key


def request_to_yandex(lat, lon):
    yandex_url = f"https://api.weather.yandex.ru/v2/forecast"
    params = {
        'lat': lat,
        'lon': lon,
        'lang': 'ru_RU',
        'limit': 1,
        'hours': False,
        'extra': False
    }
    headers = {"X-Yandex-API-Key": key}
    response = requests.get(yandex_url, params=params, headers=headers)
    data = response.json()
    # print(data)

    temperature = data['fact']['temp']
    pressure = data['fact']['pressure_mm']
    wind_speed = data['fact']['wind_speed']

    return {'temperature': temperature, 'pressure': pressure, 'wind_speed': wind_speed}
