from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    api_key = '486dd7a21e6ea691d2613e20deb310a7'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    data = response.json()

    if data['cod'] == '404':
        weather_info = 'City not found!'
    else:
        weather = data['weather'][0]['main']
        description = data['weather'][0]['description']
        temperature = data['main']['temp']
        weather_info = f'Weather: {weather}, Description: {description}, Temperature: {temperature}K'

    return render_template('index.html', weather_info=weather_info)