#!/usr/bin/env python3


import requests
from io import StringIO
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from HPAI_maps.State_Conversion import state_conversion


"""
File name: HPAI_Animal_map.py
Author: Debra Pacheco
Created: 1/21/25
Editor: Sarah Schoem
Edited: 2/13/25
Version: 1.3
Description:
    This script displays a choropleth map of the United States containing highly pathogenic avian influenza (HPAI)
    animal cases obtained from the Aphis USDA website and filtered by year.

License: MIT License
"""

def generate_animal_map():
    # Function to generate and return the map that can be used in Main file

    # Detection of Highly Pathogenic Avian Influenza in captive and wild mammals obtained from the USDA website May 2022 to present
    url = "https://www.aphis.usda.gov/sites/default/files/hpai-mammals.csv"  # HPAI_maps Detections in mammals from USDA

    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes

    # Read the content directly into a pandas DataFrame
    data = pd.read_csv(StringIO(response.text))

    #print(data.tail(30))  # Display the first few rows

    """
    ***Data Manipulation***
    """

    # Create a column containing just the year
    data['Year'] = pd.DatetimeIndex(data['Date Detected']).year

    # Create new column in data with the state abbreviation for Choropleth plotting
    data['Abbreviation'] = data['State'].apply(state_conversion)

    # Create a new data frame with state counts per year
    counts_year = data.groupby(['Abbreviation', 'Year']).size().reset_index(name='State_Count')

    # Create new data frame with total state counts
    counts_total = data.groupby(['Abbreviation']).size().reset_index(name='State_Count')

    print(data.head())

    """
    ***Map Plotting***
    """

    # Create Figure
    fig = go.Figure()

    # Add traces for each year
    years = sorted(data['Year'].unique(), reverse=True)
    for year in years:
        # Filter the data for the specific year
        yearly_data = counts_year[counts_year['Year'] == year]

        # Add choropleth trace for the year
        fig.add_trace(go.Choropleth(
            locations=yearly_data['Abbreviation'],
            z=yearly_data['State_Count'],
            locationmode="USA-states",
            colorscale="portland",
            colorbar_title="Count",
            name="",
            visible=(year == years[0])  # Only the last year is visible by default
        ))

    # Add dropdown menu
    dropdown_buttons = [
        dict(
            label=str(year),
            method="update",
            args=[{"visible": [year == y for y in years]},  # Toggle visibility of traces
                  {"title": f"State Cases of Highly Pathogenic Avian Influenza (HPAI) in Wild Mammals- {year}"}]
        )
        for year in years
    ]

    # Update layout with dropdown menu and title
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=dropdown_buttons,
                direction="down",
                showactive=True,
                x=0.5,
                y=1.2,
                xanchor="right",
                yanchor="top"
            )
        ],
        title=("State Cases of Highly Pathogenic Avian Influenza in Wild Mammals- Current Year"),
        geo=dict(scope="usa", projection={"type": "albers usa"})
    )

    return fig
