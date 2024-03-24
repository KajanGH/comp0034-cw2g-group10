import pydeck as pdk
import pandas as pd
import numpy as np

# Define the data URL
data_url = 'https://raw.githubusercontent.com/KajanGH/data/main/fem.json'

# Function to calculate sum of ages within a range
def calculate_elevation_in_range(d, start_age, end_age):
    sum = 0
    for i in range(start_age, end_age + 1):
        sum += d[f'age_{i}'] if f'age_{i}' in d else 0
    return sum

# Function to find the maximum elevation value in the provided data
def find_scale(data, start_age, end_age):
    max_val = 0
    for d in data:
        elevation = calculate_elevation_in_range(d, start_age, end_age)
        max_val = max(max_val, elevation)
    return 40000 / max_val  # Adjusted as per your requirement


# Fetch the data first
data = pd.read_json(data_url)

# Define start and end age
start_age = 0
end_age = 5

# Create Pydeck layer
layer = pdk.Layer(
    'ColumnLayer',
    data=data,
    disk_resolution=12,
    radius=1000,
    elevation_scale=find_scale(data, start_age, end_age),
    get_position='[Longitude, Latitude]',
    get_fill_color='[255, 255, 255]',  # You need to adapt this based on your ryb2rgb function
    get_elevation='calculate_elevation_in_range(d, start_age, end_age)'
)

# Create Pydeck visualization
view_state = pdk.ViewState(
    longitude=-1.932311,
    latitude=51.923,
    pitch=60,
    bearing=-32,
    min_zoom=5,
    zoom=7
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/dark-v10',
    mapbox_key='pk.eyJ1IjoiZGlhbmFtZW93IiwiYSI6ImNqcmh4aWJnOTIxemI0NXA0MHYydGwzdm0ifQ.9HakB25m0HLT-uDY2yat7A'  # Replace with your Mapbox API key
)

r.show()
