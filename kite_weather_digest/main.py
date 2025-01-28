import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import windguru_scrape

def get_next_five_weekdays():
    # Get the current date
    current_date = datetime.now()

    # List to store the next five weekdays
    next_five_weekdays = []

    # Loop to add the next five weekdays to the list
    for _ in range(5):
        next_five_weekdays.append(current_date.strftime('%A'))
        current_date += timedelta(days=1)

    return next_five_weekdays

# Get the list of next five weekdays
weekdays_list = get_next_five_weekdays()

bft_knot_conversion_table = {
    "1": "1-3 knots",
    "2": "4-6 knots",
    "3": "7-10 knots",
    "4": "11-16 knots",
    "5": "17-21 knots",
    "6": "22-27 knots",
    "7": "28-33 knots",
    "8": "34-40 knots",
    "9": "41-47 knots",
    "10": "48-55 knots",
    "11": "56-63 knots",
    "12": "64+ knots"
}

def download_image(url, file_name):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return save_path
    return None

def convert_bft_knots(bft: str) -> str:
    return bft_knot_conversion_table[bft[0]]




def scrape_lake_silvaplana(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # extract all windspeeds as strings, e.g. '5-6 bft
    windspeed = [windspeed.get_text().strip() for windspeed in soup.find_all('td', class_='widget-row meteo-windstaerke')]
    condition = [condition.get_text().strip() for condition in soup.find_all('td', class_='widget-row meteo-windqualitaet')]

    return list(zip(weekdays_list, windspeed, condition))


def scrape_urnersee():
    download_image('http://meteo.windsurfing-urnersee.ch/webcam_isleten.jpg', 'webcam_urnersee.png')
    windguru_scrape.take_website_snapshot('https://www.windguru.cz/station/2736', 'windguru_urnersee.png')


def scrape_foehndiagramm():
    download_image('https://www.meteocentrale.ch/uploads/pics/uwz-ch_foehn_de.png', 'foehndiagramm.png')




url_silvaplana = 'https://www.kitesailing.ch/spot/wetter-kitesurfen'




