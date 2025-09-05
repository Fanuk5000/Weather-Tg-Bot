FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    sqlite3 

WORKDIR /WEATHER_TG_BOT

COPY . .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]