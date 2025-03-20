#!/usr/bin/env python3 

"""
File name: HPAI_Human_map.py
Author: Sarah Schoem
Created: 2/13/25
Version: 2.0
Description:
    This script displays a choropleth map of the United States containing highly pathogenic avian influenza (HPAI)
    human cases obtained from the CDC website displaying cases since 2024.

License: MIT License
"""



import pandas as pd
import plotly.graph_objects as go
from HPAI_maps.State_Conversion import state_conversion
from HPAI_maps.scrape_fluview import scrape_fluview_data


def generate_human_map():
    """Generates a choropleth map for human H5 cases from CDC data."""
    fluview_data = scrape_fluview_data()  # Fetch the data

    if fluview_data is None:
        print("Failed to retrieve FluView data.")
        return None

    # Clean and preprocess the data
    fluview_data['State'] = fluview_data['State'].apply(lambda x: str(x).strip())
    fluview_data['State'] = fluview_data['State'].apply(
        lambda x: state_conversion(x).upper() if state_conversion(x) is not None else x)

    # Aggregate case counts per state
    fluview_data['Cases'] = pd.to_numeric(fluview_data['State Total'], errors='coerce').fillna(0)
    human_counts = fluview_data[['State', 'Cases']].groupby('State').sum().reset_index()

    # Create choropleth trace
    trace = go.Choropleth(
        locations=human_counts['State'],
        z=human_counts['Cases'],
        locationmode="USA-states",
        colorscale="Portland",
        colorbar_title="Case Count"
    )

    # Set up the layout for the map
    fig = go.Figure(data=[trace])
    fig.update_layout(
        title="Human H5 Cases (Since 2024)",
        geo=dict(scope='usa', projection={'type': 'albers usa'}),
    )

    return fig


if __name__ == "__main__":
    human_map = generate_human_map()
    if human_map:
        human_map.show()
