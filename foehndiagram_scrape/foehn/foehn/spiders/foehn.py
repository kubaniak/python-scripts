import scrapy
import re
import os

class FoehnSpider(scrapy.Spider):
    name = 'foehn'
    start_urls = ['https://web.archive.org/web/20120622224947/http://www.meteocentrale.ch/de/wetter/foehn-und-bise/foehn.html']
    target_url = 'https://web.archive.org/web/20230621160150/https://www.meteocentrale.ch/de/wetter/foehn-und-bise/foehn.html'
    image_number = 1
    visited_urls = []

    def parse(self, response):
        # Convert the Scrapy object to a string and extract the link using regex
        html_content = response.xpath('/html/body/div[4]/div[4]/div[2]/div[1]/div').get()
        image_url = re.search(r'src="([^"]+)"', html_content).group(1)

        if image_url:
            print("pass")
            # Add the prefix to the image URL
            full_image_url = f'https://web.archive.org{image_url}'

            # You can use scrapy's built-in file download functionality to download the image
            yield scrapy.Request(url=full_image_url, callback=self.save_image)

            # Extract the link from the previous response and follow it
            link_html = response.css(".d > td:nth-child(3) > a:nth-child(1)").get()
            full_next_link = re.search(r'href="([^"]+)"', link_html).group(1)

            # Check if the next link matches the target URL
            if full_next_link != self.target_url:
                # Follow the next link and continue scraping
                yield scrapy.Request(url=full_next_link, callback=self.parse)


        # Add the current URL to the list of visited websites
        self.visited_urls.append(response.url)

    def save_image(self, response):
        # Create the "Diagramme" folder if it doesn't exist
        folder_path = 'Diagramme'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Get the filename from the URL and save the image in the "Diagramme" folder
        filename = os.path.join(folder_path, self.enumerate_filename(response.url.split('/')[-1]))
        with open(filename, 'wb') as f:
            f.write(response.body)

        self.log(f'---SAVED FILE!--- {filename}')

    def enumerate_filename(self, filename):
        # Get the base name and extension of the filename
        base_name, extension = os.path.splitext(filename)

        # Check if the base filename already exists in the folder
        # If it does, append a number to it (e.g., (1), (2), etc.)
        index = 1
        while True:
            new_filename = f'{base_name}({index}){extension}'
            if not os.path.exists(os.path.join('Diagramme', new_filename)):
                return new_filename
            index += 1

    def closed(self, reason):
        # Write the list of visited URLs to a file named "visited_urls.txt"
        with open('visited_urls.txt', 'w') as f:
            for url in self.visited_urls:
                f.write(f'{url}\n')
