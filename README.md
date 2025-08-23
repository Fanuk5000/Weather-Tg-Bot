# Forecast telegram bot `FaneraWeather`

## Overview
This a simple telegram bot with broadcasting functional written on python language using aiogram framework. The bot shows future weather reports and have build in timer notification.

## Features
- Getting weather information in certain city
- A location can be saved to consistent usage
- In the bot, timers are available to set a periodical time to receive weather information
- Weather is available as by commands as by buttons

## Requirements
- Python 3.10 and higher
- Required libraries listed in `requirements.txt`
- Created config.env with `OPEN_WEATHER_TOKEN` and `TELEGRAM_BOT_TOKEN`
- sqlite to check DB manually

# Installation
1. Clone the repository or download source code
2. Navigate to the project directory
3. Create config.env file here and add inside your api tokens from [OpenWeather](https://openweathermap.org/) and [father telegram bot](https://t.me/BotFather) as OPEN_WEATHER_TOKEN=`OpenWeather token` and TELEGRAM_BOT_TOKEN=`Telegram bot token`
4. Install all dependencies by command:
    ```
    pip install -r requirements.txt
    ```

# Usage
- To run the bot, use the following command in terminal:
    ```
    python main.py
    ```
- Disable bot with `ctrl + c` command or stop by closing terminal where it is running

# Notes
- To reset Data base uncomment for once line 29 in database/models.py