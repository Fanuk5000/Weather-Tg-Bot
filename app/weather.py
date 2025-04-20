import aiohttp

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
                        print(f"Coordinates for {city}:")
                        print(f"Latitude: {lat}")
                        print(f"Longitude: {lon}")
                        return lat, lon
                    else:
                        print(f"No location found for city: {city}")
                        return None, None
                else:
                    print(f"Error fetching coordinates: HTTP {response.status}")
                    return None, None
    except Exception as e:
        print("Error fetching coordinates:", e)
        return None, None


async def get_current_weather(city: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.openweathermap.org/data/2.5/weather",
                params={"q": city, "appid": _open_weather_token, "units": "metric"}
            ) as response:
                if response.status == 200: #success
                    data = await response.json()
                    if "main" in data and "temp" in data["main"]:
                        return str(data["main"]["temp"])
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