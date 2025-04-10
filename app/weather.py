import aiohttp

async def get_weather(city: str):
    open_weather_token = "68cfa9ce6e82a3380e78a50301f5c637"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.openweathermap.org/data/2.5/weather",
                params={"q": city, "appid": open_weather_token, "units": "metric"}
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