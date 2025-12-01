# weather/views.py
import requests
from django.shortcuts import render
import datetime

# ---------------------------------------------------------
# API KEYS
# ---------------------------------------------------------
WEATHER_API_KEY = "YOUR_API_KEY"
UNSPLASH_ACCESS_KEY = "YOUR_API_KEY"


# ---------------------------------------------------------
# FUNCTION: Unsplash background image
# ---------------------------------------------------------
def get_city_image(city, weather_description):
    desc = (weather_description or "").lower()

    # Match weather to image search terms
    if "rain" in desc:
        query = f"{city} rainy skyline"
    elif "snow" in desc:
        query = f"{city} snowy skyline"
    elif "cloud" in desc:
        query = f"{city} cloudy skyline"
    elif "clear" in desc or "sunny" in desc:
        query = f"{city} sunny skyline"
    elif "storm" in desc or "thunder" in desc:
        query = f"{city} thunderstorm skyline"
    elif "fog" in desc or "mist" in desc:
        query = f"{city} foggy skyline"
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
        response = requests.get(url, params=params, timeout=8).json()
        results = response.get("results", [])
        if results:
            return results[0]["urls"]["regular"]

        # fallback to generic skyline
        params["query"] = f"{city} skyline"
        fallback = requests.get(url, params=params, timeout=8).json()
        if fallback.get("results"):
            return fallback["results"][0]["urls"]["regular"]

        return "/static/images/default.jpg"

    except Exception:
        return "/static/images/default.jpg"


# ---------------------------------------------------------
# MAIN VIEW
# ---------------------------------------------------------
def index(request):
    city = request.GET.get("city", "Toronto").strip() or "Toronto"

    # ---------------------------
    # 1. Current Weather
    # ---------------------------
    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={WEATHER_API_KEY}&units=metric"
    )

    try:
        r = requests.get(weather_url, timeout=8)
        r.raise_for_status()
        data = r.json()
    except:
        return render(request, "weather/index.html", {
            "error": "Unable to contact weather service."
        })

    if str(data.get("cod")) != "200":
        return render(request, "weather/index.html", {
            "error": data.get("message", "City not found.")
        })

    main = data.get("main", {})
    w = data.get("weather", [{}])[0]
    wind = data.get("wind", {})
    sys = data.get("sys", {})
    coord = data.get("coord", {})

    # Local Time
    offset = data.get("timezone", 0)
    now_utc = datetime.datetime.utcnow()
    local_time = now_utc + datetime.timedelta(seconds=offset)

    # Sunrise / Sunset
    sunrise = datetime.datetime.utcfromtimestamp(sys.get("sunrise") + offset).strftime("%I:%M %p")
    sunset = datetime.datetime.utcfromtimestamp(sys.get("sunset") + offset).strftime("%I:%M %p")

    # Visibility (meters → km)
    visibility_km = round(data.get("visibility", 0)/1000, 1)

    weather = {
        "city": data.get("name", city),
        "country": sys.get("country"),
        "temp": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "humidity": main.get("humidity"),
        "pressure": main.get("pressure"),
        "visibility": visibility_km,
        "description": w.get("description"),
        "wind": wind.get("speed"),
        "icon": w.get("icon") or "01d",
        "local_time": local_time.strftime("%Y-%m-%d %I:%M %p"),
        "sunrise": sunrise,
        "sunset": sunset,
        "lat": coord.get("lat"),
        "lon": coord.get("lon"),
    }

    # ---------------------------
    # 2. Forecast
    # ---------------------------
    forecast_url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={WEATHER_API_KEY}&units=metric"
    )

    forecast_list = []
    hourly_list = []

    try:
        fr = requests.get(forecast_url, timeout=8).json()
        if str(fr.get("cod")) == "200":
            entries = fr.get("list", [])

            # DAILY FORECAST (every 8th entry)
            for i in range(0, min(40, len(entries)), 8):
                item = entries[i]
                day = datetime.datetime.fromtimestamp(item["dt"]).strftime("%A")
                forecast_list.append({
                    "day": day,
                    "temp": item["main"]["temp"],
                    "description": item["weather"][0].get("description"),
                    "icon": item["weather"][0].get("icon") or "01d",
                })

            # HOURLY FORECAST (next 12 hours)
            for h in entries[:6]:  # 6 entries ≈ 18 hours
                hourly_list.append({
                    "time": datetime.datetime.fromtimestamp(h["dt"]).strftime("%I %p"),
                    "temp": h["main"]["temp"],
                    "icon": h["weather"][0].get("icon") or "01d",
                })

    except:
        forecast_list = []
        hourly_list = []

    # ---------------------------
    # 3. Background Image
    # ---------------------------
    bg_image = get_city_image(city, weather["description"])

    # ---------------------------
    # 4. Render
    # ---------------------------
    return render(request, "weather/index.html", {
        "weather": weather,
        "forecast": forecast_list,
        "hourly": hourly_list,
        "bg_image": bg_image,
    })
