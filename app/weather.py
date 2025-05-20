import aiohttp
from datetime import datetime, timedelta

from os import getenv
from dotenv import load_dotenv

load_dotenv("config.env")
OPEN_WEATHER_TOKEN = getenv("OPEN_WEATHER_TOKEN")

async def get_city_coordinates(city: str) -> tuple:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.openweathermap.org/geo/1.0/direct",
                params={"q": city, "limit": 1, "appid": OPEN_WEATHER_TOKEN}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data:
                        lat = data[0]['lat']
                        lon = data[0]['lon']
                        return str(lat), str(lon)
                    else:
                        print(f"get_city_coordinates: No location found for city: {city}")
                        return None, None
                else:
                    print(f"get_city_coordinates: Error fetching coordinates: HTTP {response.status}")
                    return None, None
    except Exception as e:
        print("get_city_coordinates: Error fetching coordinates:", e)
        return None, None


async def get_current_weather(city: str) -> dict:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.openweathermap.org/data/2.5/weather",
                params={"q": city, "appid": OPEN_WEATHER_TOKEN, "units": "metric", "lang": "ua"}
            ) as response:
                dict_info = {}
                
                if response.status == 200: #success
                    data = await response.json()
                    if "main" in data and "temp" in data["main"]:
                        
                        dict_info = {"temp": round(data["main"]["temp"]), "description": data["weather"][0]["description"]}
                        
                        return dict_info
                    else:
                        return f"get_current_weather: Unexpected response structure: {data}"
                elif response.status == 404: #no such page
                    return "get_current_weather: City not found"
                elif response.status == 429: #too much requests
                    return "get_current_weather: Rate limit exceeded. Please try again later."
                else:
                    return f"Error: {response.status} - {await response.text()}"
    except aiohttp.ClientError as ex:
        return f"get_current_weather: Network error: {ex}"
    except Exception as ex:
        return f"get_current_weather: An unexpected error occurred: {ex}"

async def get_tomorrow_weather(city) -> dict:
    lat, lon = await get_city_coordinates(city)
    if lat is None or lon is None:
        return 
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.openweathermap.org/data/3.0/onecall",
                params={"lat": lat, "lon": lon, "appid": OPEN_WEATHER_TOKEN, "exclude": "minutely,daily,current,alerts", "units": "metric", "lang": "ua" }
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    hourly = data['hourly']

                    # Get tomorrow's date
                    global tomorrow_date
                    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')
                    days_dict = {}

                    
                    for entry in hourly:
                        dt = datetime.fromtimestamp(entry['dt'])
                        date_str = dt.strftime('%d-%m-%Y')
                        time_str = dt.strftime('%H:%M')

                        # Filter for tomorrow's datej
                        if date_str == tomorrow_date:
                            temp = round(entry['temp'])
                            desc = entry['weather'][0]['description']
                        
                            if date_str not in days_dict:
                                days_dict[date_str] = []
                                                
                            days_dict[date_str].append(f"{time_str} — {temp}°C — {desc.capitalize()}")
                        
                        if date_str > tomorrow_date:
                            break

                    return days_dict.get(tomorrow_date, ["No weather data available for tomorrow."])
                
                elif response.status == 404: #no such page
                    return "City not found"
                elif response.status == 429: #too much requests
                    return "Rate limit exceeded. Please try again later."
                else:
                    return f"Error: {response.status} - {await response.text()}"
    except aiohttp.ClientError as ex:
        return f"Network error: {ex}"
    except Exception as ex:
        return f"An unexpected error occurred: {ex}"
    
async def get_weather_for_3_days(city: str) -> dict:
    lat, lon = await get_city_coordinates(city)
    if lat is None or lon is None:
        return 
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.openweathermap.org/data/3.0/onecall",
                params={"lat": lat, "lon": lon, "appid": OPEN_WEATHER_TOKEN, "exclude": "minutely,hourly,current,alerts", "units": "metric", "lang": "ua"}
            ) as response:
                if response.status == 200: #success
                    days_dict = {}
                    data = await response.json()
                    
                    for days in data["daily"][1:4]:
                        dt = datetime.fromtimestamp(days['dt'])
                        date_str = dt.strftime('%d-%m-%Y')
                        
                        if date_str not in days_dict:
            
                            morning = round(days['temp']['morn'])
                            day = round(days['temp']['day'])
                            evening = round(days['temp']['eve'])
                            night = round(days['temp']['night'])
                            desc = "Впродовж дня "+days['weather'][0]['description']
                            
                            days_dict[date_str] = (f"Ранок - {morning}°C\n День - {day}°C\n Вечір - {evening}°C\n Ніч - {night}°C\n {desc.capitalize()}")

                    
                    return days_dict
                    
                elif response.status == 404: #no such page
                    return "City not found"
                elif response.status == 429: #too much requests
                    return "Rate limit exceeded. Please try again later."
                else:
                    return f"Error: {response.status} - {await response.text()}"
    except aiohttp.ClientError as ex:
        return f"Network error: {ex}"
    except Exception as ex:
        return f"An unexpected error occurred: {ex}"

# async def get_tomorrow_weather(city) -> list:
#     lat, lon = await get_city_coordinates(city)
#     if lat is None or lon is None:
#         return 



# def get_tomorrow_weather(lat, lon):
#     url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,daily,current,alerts&appid={OPEN_WEATHER_TOKEN}&units=metric"
    
#     try:
#         response = requests.get(url)
#         data = response.json()
#         hourly = data['hourly']
#         print(f"\n[ {name} - Tomorrow's Weather ]\n")

#         # Get tomorrow's date
#         tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')
#         days_dict = {}

#         count = 0
        
#         for entry in hourly[::3]:
#             dt = datetime.fromtimestamp(entry['dt'])
#             date_str = dt.strftime('%d-%m-%Y')
#             time_str = dt.strftime('%H:%M')

#             # Filter for tomorrow's date
#             if date_str == tomorrow_date:
#                 temp = round(entry['temp'], 1)
#                 desc = entry['weather'][0]['description']

#                 if date_str not in days_dict:
#                     days_dict[date_str] = []

#                 days_dict[date_str].append(f"{time_str} — {temp}°C — {desc}")

#         # Print tomorrow's weather
#         for date, entries in days_dict.items():
#             print(f"\n{date}")
#             for line in entries:
#                 print("  " + line)

#     except Exception as e:
#         print("Error getting tomorrow's weather:", e)