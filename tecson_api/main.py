from get_weather_data import get_weather_data
import json

get_weather_data(days=20, station='tiefenbrunnen')

# Load the JSON data from the file
with open('weather_data.json', 'r') as infile:
    data = json.load(infile)





# Access the "value" inside "air_temperature" for the first entry in the "result" array
first_entry = data['result'][20]
air_temperature_value = first_entry['values']['air_temperature']['value']

print("Air Temperature Value:", air_temperature_value)
