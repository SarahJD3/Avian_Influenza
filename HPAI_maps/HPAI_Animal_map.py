#!/usr/bin/env python3

"""
File name: HPAI_Animal_map.py
Author: Debra Pacheco
Created: 1/21/25
Editor: Sarah Schoem
Last Edited: 3/9/2025
Version: 1.3
Description:
    This script displays a choropleth map of the United States containing highly pathogenic avian influenza (HPAI)
    animal cases obtained from the Aphis USDA website and filtered by year.

License: MIT License
"""

import requests
from io import StringIO
import plotly.graph_objects as go
import pandas as pd
from HPAI_maps.State_Conversion import state_conversion


def fetch_usda_data():
    """Fetches and processes HPAI cases in wild mammals from USDA APHIS."""
    url = "https://www.aphis.usda.gov/sites/default/files/hpai-mammals.csv"
    response = requests.get(url)
    response.raise_for_status()
    data = pd.read_csv(StringIO(response.text))
    data['Year'] = pd.DatetimeIndex(data['Date Detected']).year
    data['Abbreviation'] = data['State'].apply(state_conversion)
    return data.groupby(['Abbreviation', 'Year']).size().reset_index(name='State_Count')


def fetch_cdc_livestock_data():
    """Fetches and processes HPAI cases in avian livestock from the CDC website."""
    url = "https://www.cdc.gov/bird-flu/modules/situation-summary/commercial-backyard-flocks.csv"
    response = requests.get(url)
    response.raise_for_status()
    data = pd.read_csv(StringIO(response.text))
    data['Year'] = pd.to_datetime(data['Outbreak Date'], format='mixed').dt.year #different date format than aphis website
    data['Abbreviation'] = data['State'].apply(state_conversion)
    return data.groupby(['Abbreviation', 'Year']).size().reset_index(name='Livestock_Count')


def generate_animal_map():
    """Generates a choropleth map displaying HPAI cases in both wild mammals and livestock."""
    wild_mammal_data = fetch_usda_data()
    livestock_data = fetch_cdc_livestock_data()

    # Merge both datasets
    merged_data = pd.merge(wild_mammal_data, livestock_data, on=['Abbreviation', 'Year'], how='outer').fillna(0)

    fig = go.Figure()
    years = sorted(merged_data['Year'].unique(), reverse=True)

    for year in years:
        yearly_data = merged_data[merged_data['Year'] == year]
        fig.add_trace(go.Choropleth(
            locations=yearly_data['Abbreviation'],
            z=yearly_data['State_Count'],
            locationmode="USA-states",
            colorscale="portland",
            colorbar_title="Wild Mammal Cases",
            name=f"Wild Mammals {year}",
            visible=(year == years[0])
        ))
        fig.add_trace(go.Choropleth(
            locations=yearly_data['Abbreviation'],
            z=yearly_data['Livestock_Count'],
            locationmode="USA-states",
            colorscale="blues",
            colorbar_title="Livestock Cases",
            name=f"Livestock {year}",
            visible=False
        ))

    dropdown_buttons = [
                           dict(label=f"Wild Mammals {year}", method="update",
                                args=[{"visible": [(i % 2 == 0) and (i // 2 == j) for i in range(2 * len(years))]},
                                      {"title": f"HPAI Cases in Wild Mammals - {year}"}])
                           for j, year in enumerate(years)
                       ] + [
                           dict(label=f"Livestock {year}", method="update",
                                args=[{"visible": [(i % 2 == 1) and (i // 2 == j) for i in range(2 * len(years))]},
                                      {"title": f"HPAI Cases in Avian Livestock - {year}"}])
                           for j, year in enumerate(years)
                       ]

    fig.update_layout(
        updatemenus=[dict(
            active=0,
            buttons=dropdown_buttons,
            direction="down",
            showactive=True,
            x=0.5,
            y=1.2,
            xanchor="right",
            yanchor="top"
        )],
        title="HPAI Cases in Animals - Select Year and Category",
        geo=dict(scope="usa", projection={"type": "albers usa"})
    )

    return fig
