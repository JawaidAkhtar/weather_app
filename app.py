from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    api_key = '0be658e97fe65173dcdd1948b80fcbec'
    weather_data = get_weather_data(city, api_key)
    return render_template('index.html', weather=weather_data)

def get_weather_data(city, api_key):
    # Current weather data
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    
    # Check if city is found
    if data['cod'] != 200:
        return None

    # Retrieve timezone offset from API response
    timezone_offset = data['timezone']
    city_timezone = pytz.FixedOffset(timezone_offset / 60)

    # Current time in UTC
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)

    # Convert UTC time to city's local time
    local_time = utc_now.astimezone(city_timezone)

    # Next day forecast data
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()

    # Get next day forecast
    current_time = local_time
    next_day = current_time + timedelta(days=1)
    next_day_weather = None

    for forecast in forecast_data['list']:
        forecast_time = datetime.fromtimestamp(forecast['dt'], tz=pytz.utc).astimezone(city_timezone)
        if forecast_time.date() == next_day.date():
            next_day_weather = {
                'temperature': forecast['main']['temp'],
                'description': forecast['weather'][0]['description'],
                'icon': forecast['weather'][0]['icon']
            }
            break

    return {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon'],
        'day': current_time.strftime('%A'),
        'date': current_time.strftime('%Y-%m-%d'),
        'time': current_time.strftime('%H:%M:%S'),
        'next_day_weather': next_day_weather
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
