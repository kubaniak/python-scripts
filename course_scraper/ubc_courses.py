import requests
from bs4 import BeautifulSoup
import json

# Function to scrape data from a UBC course URL
def scrape_courses(url):
    data = {}
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract subject title
        subject_code_title = soup.find('h1')[0].strip()  # Extract "ENPH - Engineering Physics"
        data['subject_title'] = f"{subject_code_title}"
        
        # Extract all course titles
        courses = soup.find_all('td')
        course_list = []
        for course in courses:    
            course_list.append(course.text.strip())
        
        data['courses'] = course_list
        return data
    
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Main script
def main():
    input_file = "ubc_urls.txt"  # File containing URLs
    output_file = "courses.json"  # JSON output file
    
    try:
        # Read URLs from the file
        with open(input_file, 'r') as file:
            urls = [line.strip() for line in file.readlines()]
        
        # Scrape data for each URL
        all_courses = []
        for url in urls:
            print(f"Scraping {url}...")
            course_data = scrape_courses(url)
            if course_data:
                all_courses.append(course_data)
        
        # Save data to JSON
        with open(output_file, 'w') as json_file:
            json.dump(all_courses, json_file, indent=4)
        
        print(f"Scraped data saved to {output_file}.")
    
    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    # main()
    url = "https://courses.students.ubc.ca/browse-courses/subject/ENPH_V"
    try:
            response = requests.get(url)
            response.raise_for_status()
    except Exception as e:
            print(f"Error scraping {url}: {e}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Save the prettified soup to an HTML file
    with open("output.html", "w", encoding='utf-8') as file:
        file.write(soup.prettify())

    subject_code_title = soup.find('h1').text.strip()
    print(subject_code_title) # works

    courses = soup.find_all("subjects-courses")
    courses = soup.css.select('subjects-courses__table')
    print(courses) # doesn't work



'''.MuiTable-root'''

