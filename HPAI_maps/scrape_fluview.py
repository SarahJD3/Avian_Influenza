#!/usr/bin/env python3

"""
File name: scrape_fluview.py
Author: Sarah Schoem
Created: 2/13/25
Version: 2.0
Description:
    This script displays a choropleth map of the United States containing highly pathogenic avian influenza (HPAI)
    human cases obtained from the CDC website displaying cases since 2024.

License: MIT License
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

def scrape_fluview_data():
    # Fetch the webpage
    url = 'https://www.cdc.gov/bird-flu/situation-summary/index.html'
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the section related to "Exposure Source" and get the next table
    section = soup.find(string="Exposure Source")
    if section:
        table = section.find_next('table')
        if table:
            # Convert the table to a DataFrame using StringIO
            html_content = str(table)
            table_data = StringIO(html_content)
            df = pd.read_html(table_data)[0]

            # Clean the DataFrame (e.g., removing empty rows, renaming columns, etc.)
            df.columns = ['State', 'Dairy Herds (Cattle)', 'Poultry Farms and Culling Operations', 
                          'Other Animal Exposure', 'Exposure Source Unknown', 'State Total']
            df = df.dropna()  # Drop any rows with NaN values if they exist
        
            return df  # Return the cleaned DataFrame
        else:
            print("No table found after 'Exposure Source'.")
            return None
    else:
        print("Couldn't find 'Exposure Source' section.")
        return None
