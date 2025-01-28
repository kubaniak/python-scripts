import pandas as pd
import requests
from stationen_abk import get_station_conversion_table

def get_aktuelle_messwerte() -> pd.DataFrame:
    '''
    Gets the aktuelle Messwerte of all meteoSwiss stations
    Included in the file: Air Temperature, Sunshine Duration, Wind Direction, Wind Speed, Gusts, Air Pressure
    '''

    url = 'https://data.geo.admin.ch/ch.meteoschweiz.messwerte-aktuell/VQHA80.csv'

    station_conversion_table = get_station_conversion_table()

    # Send a request to get the content of the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Read the content of the response and create a DataFrame
        df = pd.read_csv(url, delimiter=';')
        
        # List of columns to drop
        columns_to_drop = ['rre150z0', 'gre000z0', 'ure200s0', 'tde200s0', 'pp0qffs0', 'pp0qnhs0',
                        'ppz850s0', 'ppz700s0', 'ta1tows0', 'uretows0', 'tdetows0', 'dv1towz0', 
                        'fu3towz0', 'fu3towz1']
        
        # Drop the specified columns
        df = df.drop(columns=columns_to_drop, axis=1)

        df = df.rename(columns={
            'tre200s0': 'Air Temperature [°C]',
            'sre000z0': 'Sunshine Duration [min]',
            'dkl010z0': 'Wind Direction [°]',
            'fu3010z0': 'Wind Speed [km/h]',
            'fu3010z1': 'Gusts [km/h]',
            'prestas0': 'Air Pressure [hPa]'
        })
        
        df = df[df['Air Temperature [°C]'] != '-']

        # Map the station abbreviations to station names using the dictionary
        df['Station'] = df['Station/Location'].map(station_conversion_table)

        # Convert the 'Date/Time' column to a datetime object and then format it
        df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d%H%M').dt.strftime('%Y-%m-%d %H:%M')
        
        # Drop the 'Station Abbreviation' column as it is no longer neededP
        df.drop(columns=['Station/Location'], inplace=True)
        
        # Move the 'Station' column to the first index
        station_col = df.pop('Station')
        df.insert(0, 'Station', station_col)

        # # Save the modified DataFrame to a CSV file named "data.csv" in the current directory:
        # df.to_csv('aktuelle_messwerte.csv', index=False)
        return df

        # print("CSV file downloaded, columns dropped, and saved successfully!")
    else:
        print(f"Failed to download the CSV file. Status code: {response.status_code}")
