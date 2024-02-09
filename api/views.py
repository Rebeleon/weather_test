from datetime import datetime, timedelta
from request_to_yandex import request_to_yandex
from city_lan_lat import city_lan_lat

from django.http import JsonResponse

weather_cache = {}


def get_weather(city):
    if city in weather_cache:
        cached_weather = weather_cache[city]
        if datetime.now() < cached_weather['expires']:
            return cached_weather['data']

    lan_lat = city_lan_lat(city)
    if lan_lat:
        data = request_to_yandex(lan_lat[0], lan_lat[1])
    else:
        return None

    expires = datetime.now() + timedelta(minutes=30)
    weather_cache[city] = {'data': data, 'expires': expires}

    return data


def weather_view(request):
    city = request.GET.get('city')

    if not city:
        return JsonResponse({'error': 'Missing city parameter'}, status=400)

    weather_data = get_weather(city)
    if weather_data:
        return JsonResponse(weather_data)
    else:
        return JsonResponse({'error': 'No such city in DB'}, status=422)
