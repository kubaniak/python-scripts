import pandas as pd
import numpy as np
import requests
from stationen_abk import get_station_conversion_table

def get_COSMO_forecast() -> pd.DataFrame: 
    '''
    Returns a pandas dataframe from the COSMO-2E Forecast. 
    '''
    url = 'https://data.geo.admin.ch/ch.meteoschweiz.prognosen/punktprognosen/COSMO-E-all-stations.csv'

    station_conversion_table = get_station_conversion_table()

    # Send a request to get the content of the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Read the content of the response and create a DataFrame
        df = pd.read_csv(url, delimiter=';', skiprows=24)
        
        # List of columns to drop
        columns_to_drop = []
        columns_to_drop.extend([f'TOT_PREC.{number}' for number in range(1,21)])
        columns_to_drop.extend([f'RELHUM_2M.{number}' for number in range(1,21)])    
        columns_to_drop.extend(['TOT_PREC', 
                                'RELHUM_2M',
                                'Unnamed: 129'])
        
        # Drop the specified columns
        df = df.drop(columns=columns_to_drop, axis=1)

        df = df.rename(columns={
            'time': 'Date',
        })
        
        # Drop rows with missing values in the 'Station' column
        df.dropna(subset=['stn'], inplace=True)

        # Map the station abbreviations to station names using the dictionary
        df['Station'] = df['stn'].replace(station_conversion_table)

        # Convert the 'Date' column to a datetime object and then format it
        df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d %H:%M').dt.strftime('%Y-%m-%d %H:%M')
        
        # Drop the 'Station Abbreviation' column as it is no longer needed
        df.drop(columns=['stn'], inplace=True)
        
        # Move the 'Station' column to the first index
        station_col = df.pop('Station')
        df.insert(0, 'Station', station_col)

        # Select the columns for each measuring factor (temperature, wind speed, etc.)
        temperature_columns = ['T_2M']
        temperature_columns.extend([f'T_2M.{i}' for i in range(1,21)])
        wind_speed_columns = ['FF_10M']
        wind_speed_columns.extend([f'FF_10M.{i}' for i in range(1,21)])
        wind_direction_columns = ['DD_10M']
        wind_direction_columns.extend([f'DD_10M.{i}' for i in range(1,21)])
        sunshine_duration_columns = ['DURSUN']
        sunshine_duration_columns.extend([f'DURSUN.{i}' for i in range(1,21)])

        # Helper function to convert the concatenated string of values to a list of floats and calculate the average
        def calculate_average(row, columns):
            values = row[columns].str.split(',').apply(lambda x: [float(val) for val in x if val.strip()])
            return np.mean([item for sublist in values for item in sublist])
        
        # Calculate the average for each row along the selected columns
        df['Temperature [°C]'] = df.apply(calculate_average, columns=temperature_columns, axis=1)
        df['Wind Speed [m/s]'] = df.apply(calculate_average, columns=wind_speed_columns, axis=1)
        df['Wind Direction [°]'] = df.apply(calculate_average, columns=wind_direction_columns, axis=1)
        df['Sunshine Duration [s]'] = df.apply(calculate_average, columns=sunshine_duration_columns, axis=1)

        # Create a new DataFrame with only the columns for the measuring factors and their averaged values
        averages_df = df[['Station', 'Date', 'leadtime', 'Temperature [°C]', 'Wind Speed [m/s]', 'Wind Direction [°]', 'Sunshine Duration [s]']]

        return averages_df

        # # Save the modified DataFrame to a CSV file named "data.csv" in the current directory:
        # df.to_csv('modellvorhersage_COSMO-2E.csv', index=False)
        # averages_df.to_csv('modellvorhersage_COSMO-2E_averages.csv', index=False)
        
        # print("CSV file downloaded, columns dropped, and saved successfully!")
    else:
        print(f"Failed to download the CSV file. Status code: {response.status_code}")
