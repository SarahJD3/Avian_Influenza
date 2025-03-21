#!/usr/bin/env python3

"""
File name: scrape_CDC.py
Author: Sarah Schoem
Created: 2/13/25
Edited: 3/9/2025
Version: 3.0
Description:
    This script obtains Human H5 Cases in the United States from the website: https://www.cdc.gov/bird-flu/situation-summary/index.html?cove-tab=0. This ensures the case data is updated in real-time.
"""

import time
import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_next_filename(download_path, base_filename="data-table"):
    """
    Generate the next available filename by appending a number at the end.
    E.g., data-table_1.csv, data-table_2.csv, etc.
    """
    counter = 1
    while os.path.exists(os.path.join(download_path, f"{base_filename}_{counter}.csv")):
        counter += 1
    return os.path.join(download_path, f"{base_filename}_{counter}.csv")

def scrape_CDC_data():
    # Set up Selenium WebDriver using webdriver-manager to automatically manage the driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Open the target webpage
    driver.get("https://www.cdc.gov/bird-flu/situation-summary/index.html?cove-tab=0")

    # Wait for the page to load
    time.sleep(5)

    # Use WebDriverWait to wait for the CSV link/button to be clickable
    try:
        # Wait until the element is present and clickable
        csv_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'CSV')]"))
        )

        # Scroll the element into view
        ActionChains(driver).move_to_element(csv_button).perform()

        # Click the button to download the CSV
        csv_button.click()
        print("CSV file download initiated.")

    except Exception as e:
        print(f"Error: {e}. CSV link or button not found or not clickable.")

    # Wait a few seconds to ensure the download starts
    time.sleep(5)

    # Define the download path (ensure this is where Chrome saves files)
    download_path = os.path.expanduser('~') + "/Downloads/"
    downloaded_file = download_path + "data-table.csv"

    # Generate the next available file name
    final_file = get_next_filename(download_path)

    # Check if the file is fully downloaded and move it to the desired location
    retries = 10  # Retry 10 times to check if the file exists and is accessible
    for _ in range(retries):
        if os.path.exists(downloaded_file):
            # Check if the file is still being downloaded (by checking its size)
            if os.path.getsize(downloaded_file) > 0:  # If the file size is greater than 0
                # If the file exists and has data, move it to the final location
                shutil.move(downloaded_file, final_file)
                print(f"CSV file moved to: {final_file}")
                driver.quit()
                return final_file  # Return the path to the CSV file
            else:
                print("File is being downloaded, retrying...")
                time.sleep(1)
        else:
            print("File not found, retrying...")
            time.sleep(1)

    print("Failed to download CSV or file is incomplete.")
    driver.quit()
    return None

# Example usage: scrape_CDC_data()
