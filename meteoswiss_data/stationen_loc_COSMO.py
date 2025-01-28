import pandas as pd
import numpy as np
import requests
from geopy.geocoders import Nominatim

def get_COSMO_conversion_table() -> dict:
    url = 'https://data.geo.admin.ch/ch.meteoschweiz.prognosen/punktprognosen/COSMO-E-all-stations.csv'

    # Send a request to get the content of the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Read the content of the response and create a DataFrame
        df = pd.read_csv(url, delimiter=';', skipfooter=3850, skiprows=17, engine='python', index_col=0)
        
        df = df.T

        # Create the dictionary
        indicator_dict = {}
        for index, row in df.iterrows():
            longitude = float(row['Grid_longitude:'])
            latitude = float(row['Grid_latitude:'])
            indicator_dict[index] = (latitude, longitude)
        
        del indicator_dict['Unnamed: 184']
        
        def find_nearest_place(latitude, longitude):
            geolocator = Nominatim(user_agent="myGeocoder")
            location = geolocator.reverse((latitude, longitude), language='de')

            raw_address = location.raw.get('address', {})
            country_code = raw_address.get('country_code', '')

            if 'village' in raw_address:
                place = raw_address.get('village')
            elif 'city' in raw_address:
                place = raw_address.get('city')
            elif 'town' in raw_address:
                place = raw_address.get('town')
            else:
                return 'Mauvoisin'

            hamlet = raw_address.get('hamlet', '')
            tourism = raw_address.get('tourism', '')

            if country_code == 'ch':
                if tourism:
                    return f"{tourism}, {hamlet}, {place}"
                elif hamlet:
                    return f"{hamlet}, {place}"
                else:
                    return place
            else:
                if tourism:
                    return f"{tourism}, {place}, {raw_address.get('country', '')}"
                else:
                    return f"{place}, {raw_address.get('country', '')}"

        # # Create a new dictionary with indicators as keys and nearest places as values
        indicator_with_nearest_place = {}
        for indicator, (latitude, longitude) in indicator_dict.items():
            nearest_place = find_nearest_place(latitude, longitude)
            indicator_with_nearest_place[indicator] = nearest_place

        # latitude, longitude = indicator_dict['ATT']

        # print(find_nearest_place(latitude, longitude))
        return indicator_with_nearest_place
        # df.to_csv('stationen_loc.csv', index=False)
    else:
        print(f"Failed to download the CSV file. Status code: {response.status_code}")
