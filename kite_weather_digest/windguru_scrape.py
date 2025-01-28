import os
from selenium import webdriver
import time

def take_website_snapshot(url, filename, browser='firefox'):
    # Get the current working directory
    current_directory = os.getcwd()

    # Combine the current directory with the filename to get the full relative file path
    save_path = os.path.join(current_directory, filename)

    # Initialize the appropriate WebDriver based on the browser choice
    if browser.lower() == 'chrome':
        driver = webdriver.Chrome()
    elif browser.lower() == 'firefox':
        driver = webdriver.Firefox()
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    # Navigate to the URL
    driver.get(url)

    time.sleep(1)

    # Take a screenshot and save it to the specified path
    driver.save_screenshot(save_path)

    # Close the WebDriver
    driver.quit()

