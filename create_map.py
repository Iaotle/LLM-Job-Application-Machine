#!/usr/bin/env python3
from __future__ import annotations
import os
import geopy
import folium
import webbrowser

# Create a geocoder object
geolocator = geopy.Nominatim(user_agent="Job_scraper_2024")

# # Ask the user to input multiple locations separated by commas
# locations = input("Enter multiple locations separated by commas: ").split(',')

locations = [
    'Darlingstraat 983  1102MX',
    'Dennenrodepad 15   1102MW'
]
    
map = folium.Map(zoom_start=13)

# Loop through all the locations and add them to the map
for location in locations:
    location = location.strip()  # Remove extra spaces
    h = geolocator.geocode(location)
    if h:
        folium.Marker([h.latitude, h.longitude], popup=location).add_to(map)
    else:
        print(f"Location '{location}' not found!")

# Display the map
path = './location_map.html'
map.save(path)
webbrowser.open(f'file://{os.path.realpath(path)}')