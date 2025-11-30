# weather/views.py
import requests
from django.shortcuts import render
import datetime

WEATHER_API_KEY = "5e1672ba9f277b3d1aca94d1b6908b59"
UNSPLASH_ACCESS_KEY = "ffF_zWgUljHDswOuRxzPGPaSlse-_1bYgS1MdR8Bvds"


# =============================================================
# GET CITY IMAGE FROM UNSPLASH BASED ON WEATHER
# =============================================================
def get_city_image(city, weather_description):
    desc = (weather_description or "").lower()

    # Map weather description to Unsplash query
    if "rain" in desc:
        query = f"{city} rainy city skyline"
    elif "snow" in desc:
        query = f"{city} snowy skyline"
    elif "cloud" in desc:
        query = f"{city} cloudy skyline"
    elif "clear" in desc or "sunny" in desc:
        query = f"{city} sunny skyline"
    elif "thunder" in desc or "storm" in desc:
        query = f"{city} thunderstorm skyline"
    elif "fog" in desc or "mist" in desc or "haze" in desc:
        query = f"{city} foggy skyline"
    elif "wind" in desc:
        query = f"{city} windy skyline"
    else:
        query = f"{city} skyline"

    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "client_id": UNSPLASH_ACCESS_KEY,
        "orientation": "landscape",
        "per_page": 1
    }

    try:
        response = requests.get(url, params=params, timeout=8)
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            return data["results"][0]["urls"]["regular"]

        # Fallback to city skyline
        params["query"] = f"{city} skyline"
        fallback = requests.get(url, params=params, timeout=8).json()
        if "results" in fallback and len(fallback["results"]) > 0:
            return fallback["results"][0]["urls"]["regular"]

        # Default image if nothing found
        return "/static/images/default.jpg"

    except Exception:
        return "/static/images/default.jpg"


# =============================================================
# MAIN VIEW
# =============================================================
def index(request):
    city = request.GET.get("city", "Toronto").strip() or "Toronto"

    # -----------------------------
    # 1. GET CURRENT WEATHER
    # -----------------------------
    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&appid={WEATHER_API_KEY}&units=metric"
    )

    try:
        r = requests.get(weather_url, timeout=8)
        r.raise_for_status()
        rjson = r.json()
    except Exception:
        return render(request, "weather/index.html", {
            "error": "Unable to contact weather service. Try again."
        })

    if str(rjson.get("cod")) != "200":
        return render(request, "weather/index.html", {
            "error": rjson.get("message", "City not found.")
        })

    main = rjson.get("main", {})
    weather_w = rjson.get("weather", [{}])[0]
    wind = rjson.get("wind", {})
    coord = rjson.get("coord", {})

    # Calculate local time
    timezone_offset = rjson.get("timezone", 0)
    utc_now = datetime.datetime.utcnow()
    local_time = utc_now + datetime.timedelta(seconds=timezone_offset)
    formatted_time = local_time.strftime("%Y-%m-%d %I:%M %p")

    weather = {
        "city": rjson.get("name", city),
        "temp": main.get("temp"),
        "description": weather_w.get("description"),
        "humidity": main.get("humidity"),
        "wind": wind.get("speed"),
        "icon": weather_w.get("icon"),
        "local_time": formatted_time,
        "lat": coord.get("lat"),
        "lon": coord.get("lon"),
    }

    # -----------------------------
    # 2. GET 5-DAY FORECAST
    # -----------------------------
    forecast_url = (
        f"https://api.openweathermap.org/data/2.5/forecast?"
        f"q={city}&appid={WEATHER_API_KEY}&units=metric"
    )

    forecast_list = []
    try:
        fr = requests.get(forecast_url, timeout=8)
        fr.raise_for_status()
        frjson = fr.json()

        if str(frjson.get("cod")) == "200":
            entries = frjson.get("list", [])
            # Take every 8th entry (~once per day)
            for i in range(0, min(40, len(entries)), 8):
                item = entries[i]
                day = datetime.datetime.fromtimestamp(item["dt"]).strftime("%A")
                forecast_list.append({
                    "day": day,
                    "temp": item["main"].get("temp"),
                    "description": item["weather"][0].get("description"),
                    "icon": item["weather"][0].get("icon"),
                })
    except Exception:
        forecast_list = []

    # -----------------------------
    # 3. GET BACKGROUND IMAGE
    # -----------------------------
    bg_image = get_city_image(city, weather["description"])

    # -----------------------------
    # 4. RENDER TEMPLATE
    # -----------------------------
    return render(request, "weather/index.html", {
        "weather": weather,
        "forecast": forecast_list,
        "bg_image": bg_image,
    })
