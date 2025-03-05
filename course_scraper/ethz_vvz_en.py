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
    
    kursnummer_titel = soup.select_one("#contentTop > h1:nth-child(1)")
    course_info["Course Number and Title"] = kursnummer_titel.text.strip() if kursnummer_titel else "N/A"

    dozierende = soup.find("td", class_="dozierende")
    course_info["Lecturers"] = dozierende.text.strip() if dozierende else "N/A"

    kommentar1 = soup.select_one(".inside > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2)")
    course_info["Comment 1"] = kommentar1.text.strip() if kommentar1 else "N/A"

    kommentar2 = soup.find("div", class_="kommentar-lv")
    course_info["Comment 2"] = kommentar2.text.strip() if kommentar2 else "N/A"

    tag = soup.select_one("td.td-small:nth-child(1)")
    course_info["Weekday"] = tag.text.strip() if tag else "N/A"

    uhrzeit = soup.select_one("td.td-small:nth-child(2) > a:nth-child(1)")
    course_info["Time"] = uhrzeit.text.strip() if uhrzeit else "N/A"

    wo = soup.select_one("td.td-small:nth-child(3)")
    course_info["Where"] = wo.text.strip() if wo else "N/A"

    kurzbeschreibung = soup.select_one(".inside > table:nth-child(10) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)")
    course_info["Short Description"] = kurzbeschreibung.text.strip() if kurzbeschreibung else "N/A"

    kreditpunkte = None
    for tr in soup.select(".inside > table:nth-child(13) > tbody:nth-child(1) > tr"):
        if tr.select_one("td:nth-child(1)").text.strip() == "ECTS Kreditpunkte":
            kreditpunkte = tr.select_one("td:nth-child(2)")
            break
    course_info["ECTS Credits"] = kreditpunkte.text.strip() if kreditpunkte else "N/A"

    einschraenkungen = soup.select_one(".inside > table:nth-child(22) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)")
    course_info["Restrictions"] = einschraenkungen.text.strip() if einschraenkungen else "N/A"

    return course_info

def fix_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    # Clean and fix URLs
    cleaned_urls = set()
    for url in urls:
        url = url.strip()
        if 'ansicht=ALLE' not in url:
            if '?' in url:
                url += '&ansicht=ALLE'
            else:
                url += '?ansicht=ALLE'
        cleaned_urls.add(url)

    # Write cleaned URLs back to the file
    with open(file_path, 'w') as file:
        file.write('\n'.join(cleaned_urls))

fix_urls('eth_urls.txt')

# Read URLs from the urls.txt file and remove duplicates
with open("eth_urls.txt", "r", encoding="utf-8") as file:
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
