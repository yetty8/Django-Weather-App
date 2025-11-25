import requests
from django.shortcuts import render
import datetime

WEATHER_API_KEY = "5e1672ba9f277b3d1aca94d1b6908b59"
UNSPLASH_ACCESS_KEY = "3pbWlS1ILdgA3ahMpryRtU1WWcGRVZKk-8vBs-9bpcU"  # SAFE ON BACKEND ONLY

def get_city_image(city):
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": city + " skyline",
        "client_id": UNSPLASH_ACCESS_KEY,
        "orientation": "landscape",
        "per_page": 1
    }

    response = requests.get(url, params=params)

    try:
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            return data["results"][0]["urls"]["regular"]
        else:
            return "/static/images/default.jpg"   # fallback image

    except Exception:
        return "/static/images/default.jpg"
    

def index(request):
    city = request.GET.get('city', 'Toronto')

    # Weather API
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    r = requests.get(weather_url).json()

    if r.get('cod') != 200:
        return render(request, "weather/index.html", {"error": "City not found."})

    weather = {
        "city": city,
        "temp": r["main"]["temp"],
        "description": r["weather"][0]["description"],
        "humidity": r["main"]["humidity"],
        "wind": r["wind"]["speed"],
        "icon": r["weather"][0]["icon"],
    }

    # Forecast
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"
    fr = requests.get(forecast_url).json()

    forecast_list = []
    for i in range(0, 40, 8):
        item = fr["list"][i]
        day = datetime.datetime.fromtimestamp(item["dt"]).strftime("%A")
        forecast_list.append({
            "day": day,
            "temp": item["main"]["temp"],
            "description": item["weather"][0]["description"],
            "icon": item["weather"][0]["icon"],
        })

    # Unsplash background (REAL API)
    bg_image = get_city_image(city)

    return render(request, "weather/index.html", {
        "weather": weather,
        "forecast": forecast_list,
        "bg_image": bg_image
    })
