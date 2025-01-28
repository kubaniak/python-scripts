import requests
import json
from bs4 import BeautifulSoup

# Function to scrape course information from a given URL
def scrape_course_info(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page: {url}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    course_info = {}
    
    kursnummer = soup.select_one(".inside > table:nth-child(7) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1)")
    course_info["Kursnummer"] = kursnummer.text.strip() if kursnummer else "N/A"

    titel = soup.select_one(".inside > table:nth-child(7) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)")
    course_info["Titel"] = titel.text.strip() if titel else "N/A"

    dozierende = soup.find("td", class_="dozierende")
    course_info["Dozierende"] = dozierende.text.strip() if dozierende else "N/A"

    kommentar1 = soup.select_one(".inside > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2)")
    course_info["Kommentar 1"] = kommentar1.text.strip() if kommentar1 else "N/A"

    kommentar2 = soup.find("div", class_="kommentar-lv")
    course_info["Kommentar 2"] = kommentar2.text.strip() if kommentar2 else "N/A"

    tag = soup.select_one("td.td-small:nth-child(1)")
    course_info["Wochentag"] = tag.text.strip() if tag else "N/A"

    uhrzeit = soup.select_one("td.td-small:nth-child(2) > a:nth-child(1)")
    course_info["Uhrzeit"] = uhrzeit.text.strip() if uhrzeit else "N/A"

    wo = soup.select_one("td.td-small:nth-child(3)")
    course_info["Wo"] = wo.text.strip() if wo else "N/A"

    kurzbeschreibung = soup.select_one(".inside > table:nth-child(10) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)")
    course_info["Kurzbeschreibung"] = kurzbeschreibung.text.strip() if kurzbeschreibung else "N/A"

    kreditpunkte = soup.select_one(".inside > table:nth-child(13) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2)")
    course_info["Kreditpunkte"] = kreditpunkte.text.strip() if kreditpunkte else "N/A"

    einschraenkungen = soup.select_one(".inside > table:nth-child(22) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)")
    course_info["Einschränkungen"] = einschraenkungen.text.strip() if einschraenkungen else "N/A"

    return course_info

def fix_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()

    # Clean and fix URLs
    cleaned_urls = set()
    for url in urls:
        if 'ansicht=ALLE' not in url:
            # Update URL to include ansicht=ALLE
            url_parts = url.split('&')
            for i, part in enumerate(url_parts):
                if 'ansicht=' in part:
                    url_parts[i] = 'ansicht=ALLE'
            url = '&'.join(url_parts)

        cleaned_urls.add(url.strip())

    # Write cleaned URLs back to the file
    with open(file_path, 'w') as file:
        file.write('\n'.join(cleaned_urls))

fix_urls('urls.txt')

# Read URLs from the urls.txt file and remove duplicates
with open("urls.txt", "r", encoding="utf-8") as file:
    urls = list(set(url.strip() for url in file.read().splitlines()))

# Scrape course information for each URL
course_data_list = []
for url in urls:
    course_info = scrape_course_info(url)
    if course_info:
        course_data_list.append(course_info)

# Save the course data to a JSON file
with open("course_data.json", "w", encoding="utf-8") as json_file:
    json.dump(course_data_list, json_file, ensure_ascii=False, indent=4)

print("Scraping completed. Course data saved to course_data.json.")
