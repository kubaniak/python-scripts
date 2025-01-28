import csv
import os
import requests
from tqdm import tqdm

# Define the path to your CSV file
csv_file_path = 'urls.csv'

# Create a directory to save downloaded files
download_dir = 'downloads'
os.makedirs(download_dir, exist_ok=True)

# Open the CSV file and read URLs
with open(csv_file_path, 'r') as csv_file:
    reader = csv.reader(csv_file)
    urls = [row[0] for row in reader]

# Download files with a progress bar
for url in tqdm(urls, desc="Downloading files"):
    # Get the filename from the URL
    filename = os.path.basename(url)
    
    # Set the path to save the file
    file_path = os.path.join(download_dir, filename)
    
    # Download the file
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except requests.exceptions.RequestException as e:
        pass  # Handle the exception silently

