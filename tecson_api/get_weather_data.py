import requests
from datetime import datetime, timedelta
import json

def get_weather_data(
        station: str=None, 
        days: int=0,
        columnToSort: str='timestamp_cet',
        direction: str='desc',
        limit: int=1000,
        offset=0) -> None:
    '''
    Gets the weather data from either the Tiefenbrunnen of the Mythenquai tecson weather station and 
    outputs a new json file stored in the same folder. 
    '''
    if days <= 0:
        raise ValueError("Days must be > 0")


    endDate = datetime.now().strftime('%Y-%m-%d')

    startDate = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    url = f'https://tecdottir.herokuapp.com/measurements/{station}?startDate={startDate}&endDate={endDate}&sort={columnToSort}%20{direction}&limit={limit}&offset={offset}'

    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        # Handle the API response here
        # print(data)  # Uncomment this line if you want to see the original JSON output
        # Save the JSON data to a separate file with indentation for readability
        with open('weather_data.json', 'w') as outfile:
            json.dump(data, outfile, indent=2)
            print("Data saved to weather_data.json")
    else:
        # Handle any errors that occurred during the API request
        print("Error:", response.status_code, response.text)
