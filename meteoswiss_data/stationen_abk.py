import pandas as pd
import requests

def get_station_conversion_table():

    url = 'https://data.geo.admin.ch/ch.meteoschweiz.messnetz-automatisch/ch.meteoschweiz.messnetz-automatisch_de.csv'

    # Send a request to get the content of the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Read the content of the response and create a DataFrame
        df = pd.read_csv(url, delimiter=';', encoding='ISO-8859-1')
        
        # List of columns to drop
        columns_to_keep = ['Station', 'Abk.']
        
        # Drop the specified columns
        df = df[columns_to_keep]

        return df.set_index('Abk.').to_dict()['Station']

    else:
        print(f"Failed to download the CSV file. Status code: {response.status_code}")
