#!/usr/bin/env python3

"""
File name: HPAI_Human_map.py
Author: Sarah Schoem
Created: 2/13/25
Edited: 3/9/2025
Version: 3.1
Description:
    This script displays a choropleth map of the United States containing highly pathogenic avian influenza (HPAI)
    human cases obtained from the CDC website displaying cases since 2024.
"""

import pandas as pd
import plotly.graph_objects as go
import os
from HPAI_maps.State_Conversion import state_conversion
from HPAI_maps.scrape_CDC import scrape_CDC_data


def get_most_recent_csv(download_path):
    """
    Finds the most recent CSV file in the download directory.
    Assumes the filename starts with 'data-table_' and ends with '.csv'.
    """
    csv_files = [f for f in os.listdir(download_path) if f.startswith("data-table_") and f.endswith(".csv")]

    if not csv_files:
        return None

    # Get the most recent file by comparing modification times
    most_recent_file = max(csv_files, key=lambda f: os.path.getmtime(os.path.join(download_path, f)))
    return os.path.join(download_path, most_recent_file)


def generate_human_map():
    """Generates a choropleth map for human H5 cases from CDC data."""
    # Fetch the most recent data
    download_path = os.path.expanduser('~') + "/Downloads/"
    csv_file_path = get_most_recent_csv(download_path)

    if csv_file_path is None:
        print("No CSV files found.")
        return None

    print(f"Using the most recent file: {csv_file_path}")

    # Read the downloaded CSV file into a pandas DataFrame
    CDC_data = pd.read_csv(csv_file_path)

    # Clean and preprocess the data
    CDC_data['State'] = CDC_data['State'].apply(lambda x: str(x).strip())
    CDC_data['State'] = CDC_data['State'].apply(
        lambda x: state_conversion(x).upper() if state_conversion(x) is not None else x)

    # Aggregate case counts per state
    CDC_data['Cases'] = pd.to_numeric(CDC_data['State Total'], errors='coerce').fillna(0)
    human_counts = CDC_data[['State', 'Cases']].groupby('State').sum().reset_index()

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
