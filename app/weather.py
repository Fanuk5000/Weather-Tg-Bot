import aiohttp
from datetime import datetime, timedelta

_open_weather_token = "68cfa9ce6e82a3380e78a50301f5c637"

async def get_city_coordinates(city: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.openweathermap.org/geo/1.0/direct",
                params={"q": city, "limit": 1, "appid": _open_weather_token}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data:
                        lat = data[0]['lat']
                        lon = data[0]['lon']
                        return str(lat), str(lon)
                    else:
                        print(f"No location found for city: {city}")
                        return None, None
                else:
                    print(f"Error fetching coordinates: HTTP {response.status}")
                    return None, None
    except Exception as e:
        print("Error fetching coordinates:", e)
        return None, None


async def get_current_weather(city: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.openweathermap.org/data/2.5/weather",
                params={"q": city, "appid": _open_weather_token, "units": "metric"}
            ) as response:
                if response.status == 200: #success
                    data = await response.json()
                    if "main" in data and "temp" in data["main"]:
                        return str(round(data["main"]["temp"]))
                    else:
                        return f"Unexpected response structure: {data}"
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

async def get_tomorrow_weather(city) -> list:
    lat, lon = await get_city_coordinates(city)
    if lat is None or lon is None:
        return 
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.openweathermap.org/data/3.0/onecall",
                params={"lat": lat, "lon": lon, "exclude": "minutely,daily,current,alerts", "appid": _open_weather_token, "units": "metric"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    hourly = data['hourly']

                    # Get tomorrow's date
                    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')
                    days_dict = {}

                    
                    for entry in hourly[::3]:
                        dt = datetime.fromtimestamp(entry['dt'])
                        date_str = dt.strftime('%d-%m-%Y')
                        time_str = dt.strftime('%H:%M')

                        # Filter for tomorrow's date
                        if date_str == tomorrow_date:
                            temp = round(entry['temp'])
                            desc = entry['weather'][0]['description']

                            if date_str not in days_dict:
                                days_dict[date_str] = []

                            days_dict[date_str].append(f"{time_str} — {temp}°C — {desc}")

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



# def get_tomorrow_weather(lat, lon):
#     url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,daily,current,alerts&appid={open_weather_token}&units=metric"
    
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