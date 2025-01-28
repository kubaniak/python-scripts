import pandas as pd
import requests

def get_foehnindex():
    '''Gets the current Föhnindex of all Stations as a pandas dataframe'''
    
    url = 'https://data.geo.admin.ch/ch.meteoschweiz.messwerte-foehn-10min/ch.meteoschweiz.messwerte-foehn-10min_de.csv'

    # Send a request to get the content of the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Read the content of the response and create a DataFrame
        df = pd.read_csv(url, delimiter=';', encoding='ISO-8859-1')
        
        # List of columns to drop
        columns_to_keep = ['Station', 'Föhnindex', 'Messdatum']
        
        # Drop the specified columns
        df = df[columns_to_keep]

        df['Föhnindex'], df['Messdatum'] = df['Messdatum'], df['Föhnindex']    

        df = df.rename(columns={
            'Messdatum': 'Föhnindex',
            'Föhnindex': 'Date'
        })
        
        return df
    else:
        print(f"Failed to download the CSV file. Status code: {response.status_code}")